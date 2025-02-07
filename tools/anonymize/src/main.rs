use clap::{Command, Arg};
use std::{
    io::{self, Read, Write, BufRead, BufReader},
    fs::{self},
    path::Path,
    collections::HashMap
};
use sha2::{Sha256, Digest};
use unicode_bom::Bom;
use chrono::{NaiveDateTime, Datelike};

enum Input {
    File(fs::File),
    Stdin(io::Stdin),
}

impl Read for Input {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        match *self {
            Input::File(ref mut file) => file.read(buf),
            Input::Stdin(ref mut stdin) => stdin.read(buf),
        }
    }
}

fn unix_to_date_string(unix_timestamp: i64) -> String {
    let output;
    let time = NaiveDateTime::from_timestamp(unix_timestamp, 0);
    output = format!(
            "{:02}{:02}{:04}",
            time.day(),
            time.month(),
            time.year()
        ).to_string();
    return output;
}

fn read_line_lossy<R: BufRead>(reader: &mut R) -> Result<String, String> {
    let mut buf: Vec<u8> = Vec::new();
    return match reader.read_until(b'\n', &mut buf) {
        Ok(_) => {
            if buf.is_empty() {
                return Err("Reader empty".to_string());
            }
            let _ = &buf.pop();
            if buf.last() == Some(&b'\r') {
                let _ = &buf.pop();
            }
            return Ok(String::from_utf8_lossy(&buf).to_string());
        }
        Err(e) => Err(e.to_string())
    };
}

fn hash(input: impl AsRef<[u8]>) -> String {
    let mut hasher = Sha256::new();
    hasher.update(input);
    return format!("{:X}", hasher.finalize());
}

fn calculate_caseid(name: &str, surname: &str, timestamp: &str, birthday: &str) -> String{
    let input = String::from(&name[..]) + &unix_to_date_string(timestamp.parse::<i64>().unwrap()) + &surname[..] + &unix_to_date_string(birthday.parse::<i64>().unwrap());
    return hash(input);
}

fn calculate_dispatchid(vehicle: &str, timestamp: &str) -> String {
    let input = String::from(vehicle) + &unix_to_date_string(timestamp.parse::<i64>().unwrap());
    return hash(input);
}

fn main() -> Result<(), io::Error> {
    // Collect help information and arguments
    let matches = Command::new("anonymize")
        .version("0.1.1")
        .author("G. Tomšič (SiOHCA Team)")
        .about("Anonymize CSV data for posting to OHCA API Server.\nOutputs data to stdout.")
        .arg(
            Arg::new("INPUT")
                .help("Sets input file(s). - reads from stdin.")
                .allow_hyphen_values(true)
                .required(true)
                .takes_value(true)
        )
        .arg(
            Arg::new("delimiter")
                .help("Specifies delimiter.")
                .short('d')
                .long("delimiter")
                .default_value(",")
                .use_value_delimiter(false)
                .takes_value(true)
        )
        .get_matches();

    let reqs_case = ["name", "surname", "timestamp", "birthday"];
    let reqs_disp = ["vehicleID", "timestamp"];

    let columns = [
        "caseID", "dispatchID",
        "dispIdentifiedCA", "dispProvidedCPRinst",
        "age", "gender", "witnesses", "location",
        "bystanderResponse", "bystanderResponseTime",
        "bystanderAED", "bystanderAEDTime",
        "deadOnArrival", "firstMonitoredRhy",
        "pathogenesis", "independentLiving",
        "comorbidities", "vad", "cardioverterDefib",
        "stemiPresent", "responseTime", "defibTime",
        "ttm", "ttmTemp", "drugs", "airwayControl",
        "cprQuality", "shocks", "drugTimings",
        "vascularAccess", "mechanicalCPR",
        "targetVent", "reperfusionAttempt",
        "reperfusionTime", "ecls", "iabp",
        "ph", "lactate", "glucose", "neuroprognosticTests",
        "specialistHospital", "hospitalVolume", "ecg",
        "ecgBLOB", "targetBP", "survived", "rosc",
        "roscTime", "SurvivalDischarge30d",
        "cpcDischarge", "mrsDischarge",
        "survivalStatus", "transportToHospital",
        "treatmentWithdrawn", "cod", "organDonation",
        "patientReportedOutcome", "qualityOfLife"
    ];

    let delimiter = matches.value_of("delimiter").unwrap();
    let input = match matches.value_of("INPUT").unwrap() {
        "-" => {Input::Stdin(io::stdin())},
        filename => {Input::File(fs::File::open(Path::new(filename)).expect("No such file!"))}
    };

    // Read file lines as vector of bytes (by line), don't destroy non UTF8 data
    let mut reader = BufReader::new(input);
    let mut writer = io::stdout();

    let mut b_caseid = false;
    let mut b_dispid = false;

    let mut titles: HashMap<String, usize> = HashMap::new();
    let mut first_loop = true;
    loop {
        match read_line_lossy(&mut reader) {
            Ok(line) => {
                // Main program
                let data: Vec<&str> = line.split(delimiter).collect();
                let mut output: Vec<String> = Vec::new();

                // Check for BOM
                let bom = Bom::from(data[0].as_bytes());

                // Only run this on the first loop
                // Get the column titles
                if first_loop {
                    for i in 0..data.len() {
                        match i {
                            0 => {titles.insert(String::from(&data[i][bom.len()..]), i);},
                            i => {titles.insert(String::from(data[i]), i);}
                        }
                    }
                    b_caseid = reqs_case.iter().all(|item| titles.keys().collect::<Vec<_>>().contains(&&item.to_string()));
                    b_dispid = reqs_disp.iter().all(|item| titles.keys().collect::<Vec<_>>().contains(&&item.to_string()));

                    write!(writer, "{}\n", columns.join(delimiter))?;

                    first_loop = false;
                    continue;
                }

                for title in columns {
                    match title {
                        "caseID" => {
                            if b_caseid {
                                let name = data[titles["name"]];
                                let surname = data[titles["surname"]];
                                let timestamp = data[titles["timestamp"]];
                                let birthday = data[titles["birthday"]];
                                output.push(
                                    match name.len() == 0 || surname.len() == 0 || timestamp.len() == 0 {
                                        false => calculate_caseid(name, surname, timestamp, birthday),
                                        true => String::from("NULL")
                                    }
                                );
                            } else {
                                output.push(String::from("NULL"));
                            }
                        },
                        "dispatchID" => {
                            if b_dispid {
                                let vehicle = data[titles["vehicleID"]];
                                let timestamp = data[titles["timestamp"]];
                                output.push(
                                    match vehicle.len() == 0 || timestamp.len() == 0 {
                                        false => calculate_dispatchid(vehicle, timestamp),
                                        true => String::from("NULL")
                                    }
                                );
                            } else {
                                output.push(String::from("NULL"));
                            }
                        },
                        title => {
                            output.push(
                                match titles.get(title) {
                                    Some(key) => match data[key.to_owned()] {
                                            "" => String::from("NULL"),
                                            value => String::from(value)
                                        },
                                    None => String::from("NULL")
                                }
                            )
                        }
                    } 
                }

                write!(writer, "{}\n", output.join(delimiter))?;
            },
            Err(e) => {
                if &e == "Reader empty" {
                    return Ok(());
                } else {
                    eprintln!("{}", e)
                }
            }
        }
    }
}