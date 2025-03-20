use clap::{Parser, Subcommand};
use std::ffi::OsString;
use std::path::PathBuf;
use tracing::debug;
mod lager;
use regex::Regex;

#[derive(Parser, Debug)]
#[command(version, about, allow_external_subcommands = true)]
struct Cli {
    /// Sets a custom config file
    #[arg(short, long, value_name = "FILE")]
    config: Option<PathBuf>,

    /// Turn debugging information on
    #[arg(short, long, action = clap::ArgAction::SetTrue)]
    debug: bool,

    #[command(subcommand)]
    command: SubCommands,
}

#[derive(Parser, Debug)]
struct ConfigArgs {
    /// The config file to use
    #[arg(short, long)]
    file: Option<String>,
}

#[derive(Parser, Debug)]
struct ListArgs {
    /// The config file to use
    #[arg(short, long)]
    file: Option<String>,

    /// output JSON
    #[arg(short, long, action = clap::ArgAction::SetTrue)]
    json: bool,
}

#[derive(Subcommand, Debug)]
enum SubCommands {
    #[command(hide = true)]
    Config(ConfigArgs),

    /// List cv/ev/wa exes/commands
    List(ListArgs),

    #[command(
        external_subcommand,
        about = "Run an external subcommand",
        allow_hyphen_values = true
    )]
    External(Vec<OsString>),
}

// TODO: make real resolve function
fn resolve_exe_name(name: &str) -> String {
    if name == "coviz" || name == "viz" {
        return "coviz".to_string();
    }
    format!("cv_{name}")
}

fn exe_is_gui(name: &str) -> bool {
    let prefixes = ["cv_", "ev_", "wa_"];
    // stupid version if the exe starts with any of the prefixes it is not
    // a gui exe
    !prefixes.iter().any(|&p| name.starts_with(p))
}

fn find_exe(name: &str) -> anyhow::Result<PathBuf> {
    let p = which::which(name)?;
    Ok(p)
}

fn run_exe(args: &Vec<OsString>) -> anyhow::Result<()> {
    debug!("args: {:?}", args);

    let name = args[0].to_string_lossy();
    let args = &args[1..];

    debug!("name: {} ~ args: {:?}", name, args);
    let real_exe_name = resolve_exe_name(&name);
    debug!("resolved exe name: {}", real_exe_name);
    let real_exe_path = find_exe(&real_exe_name)?;
    debug!("resolved exe path: {:?}", real_exe_path);
    let is_gui = exe_is_gui(&real_exe_name);
    debug!("is gui: {}", is_gui);

    if is_gui {
        let child = std::process::Command::new(real_exe_path)
            .args(args)
            .spawn()?;
        debug!("started gui process ~ child: {:?}", child);
    } else {
        let child = std::process::Command::new(real_exe_path)
            .args(args)
            .spawn()?;
        debug!("started process ~ child: {:?}", child);

        let output = child.wait_with_output()?;
        if output.status.success() {
            println!("Output: {}", String::from_utf8_lossy(&output.stdout));
        } else {
            eprintln!("Error: {}", String::from_utf8_lossy(&output.stderr));
        }
    }

    Ok(())
}

#[derive(Debug, Clone, serde::Serialize)]
pub struct DgiExe {
    // pub name: String,
    pub path: String,
    pub is_gui: bool,
}

fn list_commands(args: &ListArgs) -> anyhow::Result<()> {
    let re = Regex::new(r"^(cv|ev|wa)_")?;
    let commands_iter = which::which_re(re)?;

    let commands: std::collections::BTreeMap<String, DgiExe> = commands_iter
        .filter_map(|path| {
            let filename = path.file_name()?.to_str()?.to_string();
            Some((filename, path))
        })
        .map(|(filename, path)| {
            // Construct the DgiExe with an owned PathBuf and a bool for is_gui.
            let dgiexe = DgiExe {
                path: path.to_string_lossy().to_string(),
                is_gui: exe_is_gui(&filename),
            };
            (filename, dgiexe)
        })
        .collect();

    if args.json {
        // Output in JSON format
        println!("{}", serde_json::to_string(&commands)?);
    } else {
        for (name, dgiexe) in &commands {
            let path_posixy = dgiexe.path.replace('\\', "/");
            println!("{name} - {path_posixy}");
        }
    }
    // Now 'commands' owns its data. No references to short-lived local variables.

    Ok(())
}

fn main_run() -> anyhow::Result<()> {
    lager::tracing_init()?;
    debug!("__DG__");
    let argv = std::env::args().collect::<Vec<String>>();
    debug!("argv: {:?}", argv);
    let cli = Cli::parse();
    debug!("cli: {:?}", cli);
    if let Some(config_path) = cli.config.as_deref() {
        eprintln!("Value for config: {}", config_path.display());
    }

    // TODO: actually do stuff to set debug
    if cli.debug {
        debug!("Debugging enabled");
    }

    match &cli.command {
        SubCommands::Config(args) => {
            debug!("Running config subcommand: {args:?}");
        }
        SubCommands::List(args) => {
            debug!("Running list subcommand: {args:?}");
            list_commands(args)?;
        }
        SubCommands::External(args) => {
            debug!("Running external subcommand: {args:?}");
            run_exe(args)?;
        }
    }

    Ok(())
}

fn main() {
    let r = main_run();
    if let Err(e) = r {
        eprintln!("Error: {e:#}");
        std::process::exit(1);
    }
    std::process::exit(0);
}
