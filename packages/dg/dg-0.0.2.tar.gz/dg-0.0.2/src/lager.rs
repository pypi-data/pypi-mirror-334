use std::str::FromStr;
use tracing::debug;
use tracing::level_filters::LevelFilter;

/// List of environment variables to check for logging level
const LOG_ENV_VARS: [&str; 3] = ["DGLOG", "DG_LOG", "RUST_LOG"];

fn env_var_is_falsey(s: &str) -> bool {
    let s_lower = s.trim().to_lowercase();
    matches!(s_lower.as_str(), "" | "0" | "false" | "off" | "no" | "n")
}

fn env_var_str_is_truthy(s: &str) -> bool {
    !env_var_is_falsey(s)
}

/// Return the EnvFilter directive to use for initializing the tracing subscriber,
/// Looks for the following environment variables, in order:
///   "DGTRACE" - truthy value enables trace logging
///   "DGDEBUG" - truthy value enables debug logging
///   "DGLOG" - returns
/// otherwise using 'RUST_LOG' if set.
fn env_log_level() -> LevelFilter {
    // use "DGTRACE" if set to a truthy value
    if let Ok(dg_trace) = std::env::var("DGTRACE") {
        if env_var_str_is_truthy(&dg_trace) {
            return LevelFilter::TRACE;
        }
    }

    if let Ok(dg_debug) = std::env::var("DGIDEBUG") {
        if env_var_str_is_truthy(&dg_debug) {
            return LevelFilter::DEBUG;
        }
    }

    if let Ok(dg_debug) = std::env::var("DGDEBUG") {
        if env_var_str_is_truthy(&dg_debug) {
            return LevelFilter::DEBUG;
        }
    }

    for env_var in LOG_ENV_VARS.iter() {
        if let Ok(value) = std::env::var(env_var) {
            if value.is_empty() {
                continue;
            }
            if env_var_is_falsey(&value) {
                continue;
            }
            match LevelFilter::from_str(&value) {
                Ok(level) => return level,
                Err(_) => {
                    return LevelFilter::DEBUG;
                }
            }
        }
    }
    LevelFilter::WARN
}

pub fn tracing_init() -> anyhow::Result<()> {
    // use "DG_LOG" if set to a truthy value, otherwise use 'RUST_LOG' if set.
    let env_log_level = env_log_level();
    debug!(
        "tracing_init - env_filter_directives_string: {}",
        env_log_level
    );
    let subscriber = tracing_subscriber::fmt()
        .with_span_events(
            tracing_subscriber::fmt::format::FmtSpan::CLOSE
                | tracing_subscriber::fmt::format::FmtSpan::ENTER,
        )
        .with_writer(std::io::stderr)
        .with_max_level(env_log_level)
        .finish();
    let set_subscriber_result = tracing::subscriber::set_global_default(subscriber);
    match set_subscriber_result {
        Ok(()) => {
            debug!("tracing_init - set_global_default succeeded");
        }
        Err(e) => {
            debug!("tracing_init - set_global_default failed: {:?}", e);
        }
    }
    Ok(())
}

// -------------------------------
// USING ENV FILTER
// -------------------------------
// pub(crate) fn init_tracing() -> anyhow::Result<()> {
//     // construct a subscriber that prints formatted traces to stdout
//     // let subscriber = tracing_subscriber::FmtSubscriber::builder().with_level(
//     // set the default level for all spans
//     // tracing::Level::DEBUG,
//     // );
//     // use that subscriber to process traces emitted after this point
//     // tracing::subscriber::set_global_default(subscriber)?;

//     let filter = EnvFilter::builder()
//         .with_default_directive(tracing_subscriber::filter::LevelFilter::WARN.into())
//         .parse(level)?;

//     let subscriber = tracing_subscriber::fmt()
//         .with_span_events(
//             tracing_subscriber::fmt::format::FmtSpan::CLOSE
//                 | tracing_subscriber::fmt::format::FmtSpan::ENTER,
//         )
//         .with_env_filter(filter)
//         .with_writer(std::io::stderr)
//         .finish();
//     tracing::subscriber::set_global_default(subscriber)?;
//     Ok(())
// }
