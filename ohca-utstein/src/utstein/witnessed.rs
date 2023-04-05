use serde::Serialize;
use sqlx::MySqlPool;

/// The Witnessed field
///
/// # Field mappings
///
/// * Bystander - `bystander` is the number of rows where `witnesses` = 1
/// * EMS - `ems` is the number of rows where `witnesses` = 2
/// * Unwitnessed - `unwitnessed` is the number of rows where `witnesses` = 0
/// * Witnessed unknown - `unknown` is the number of rows where `witnesses` = -1 or NULL
#[derive(Debug, Serialize)]
pub struct Witnessed {
    pub bystander: i64,
    pub ems: i64,
    pub unwitnessed: i64,
    pub unknown: i64,
}

impl Witnessed {
    pub async fn new(pool: &MySqlPool) -> Self {
        sqlx::query_as!(
            Witnessed,
            r#"
                SELECT
                    (SELECT COUNT(*) FROM cases WHERE witnesses = 1) AS "bystander!: i64",
                    (SELECT COUNT(*) FROM cases WHERE witnesses = 2) AS "ems!: i64",
                    (SELECT COUNT(*) FROM cases WHERE witnesses = 0) AS "unwitnessed!: i64",
                    (SELECT COUNT(*) FROM cases WHERE witnesses = -1 OR bystanderResponse IS NULL) AS "unknown!: i64"
            "#
        )
        .fetch_one(pool)
        .await
        .unwrap()
    }
}
