// Configure the Google Cloud provider
provider "google" {
  credentials = "${file("/team1/team1/squadster/client_secrets.json")}"
  project     = "squadster"
  region      = "us-central1"
}

// Create a new instance
resource "google_project" "squadster" {
  id = //insert id here
}
