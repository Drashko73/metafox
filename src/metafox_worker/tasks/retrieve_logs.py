from metafox_worker.main import app

@app.task
def retrieve_logs(job_id: str, num_of_lines: int) -> str:
    try:
        with open("metafox_worker/logs/" + job_id + ".log", "r") as f:
            lines = f.readlines()
            lines = [line for line in lines if line.strip()]    # Remove empty lines from the log file
            
            if num_of_lines == 0:
                return "".join(lines) # Return the entire log file
            
            return "".join(lines[-num_of_lines:])
    except FileNotFoundError:
        return "Log file not found."
    except Exception as e:
        return str(e)