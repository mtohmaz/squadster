provider "google" {
    credentials = "${file("SeniorDesign-3f9160f140b5.json")}"
    project = "seniordesign-143118"
    region = "us-east1-b"
}

resource "google_compute_instance" "dev-instance" {
    name = "dev-instance"
    machine_type = "custom-1-2048"
    zone = "us-east1-b"
    tags = ["dev"]
    disk {
        image = "ubuntu-os-cloud/ubuntu-1604-lts"
        size = 10
    }
    network_interface {
        network = "default"
        access_config {
            // ephemeral public ip
        }
    }
    service_account {
        email = "290427034826-compute@developer.gserviceaccount.com"
        scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    }
}
