# Pais Deals Notifier

A Python automation script that checks the Pais Plus website for deals related to a specific topic.  
If matching deals are found, the script sends an email with all the deal details.  
If no deals are found, the script sends an email stating that no matching deals were found.

## Technologies
- Python
- Selenium (for website scraping)
- SMTP (for sending emails)

## Usage
1. Set your search keyword in the code (`the_deal`).
2. Make sure you have a `config.json` file containing your sender email and password (these are not included in the repository for security reasons).
3. Run the script.
4. Receive the results via email.

## Note
The `config.json` file is **not** included in this repository and is listed in `.gitignore` because it contains sensitive credentials.  
You will need to create your own `config.json` file with the required fields before running the script:

```json
{
  "sender_email": "your_email@example.com",
  "receiver_email": "receiver_email@example.com",
  "password": "your_app_password"
}
