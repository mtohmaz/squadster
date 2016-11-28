provider "google" {
    credentials = "${file("SeniorDesign-3f9160f140b5.json")}"
    project = "seniordesign-143118"
    region = "us-east1-b"
}

resource "google_compute_target_pool" "webservers" {
    name = "squadster-webserver-pool"
    instances = [
        "${google_compute_instance.app-instance.*.self_link}"
    ]
    health_checks = [
        "${google_compute_http_health_check.default.name}"
    ]
    region = "us-east1"
}

resource "google_compute_network" "default" {
    name = "squadster-private"
    ipv4_range = "10.0.0.0/16"
}

resource "google_compute_firewall" "default" {
    name = "firewall"
    network = "${google_compute_network.default.name}"
    allow {
        protocol = "tcp"
        ports = ["80", "8080", "22"]
    }
    allow {
        protocol = "icmp"
    }
    source_tags = ["app"]
}

resource "google_compute_forwarding_rule" "default" {
    name = "fwd-rule"
    target = "${google_compute_target_pool.webservers.self_link}"
    port_range = 80
    region = "us-east1"
}

resource "google_compute_instance" "app-instance" {
    count = 3
    name = "app-instance-${count.index}"
    machine_type = "custom-1-2048"
    zone = "us-east1-b"
    tags = ["app"]
    disk {
        image = "ubuntu-os-cloud/ubuntu-1604-lts"
        size = 10
    }
    network_interface {
        network = "squadster-private"
    }
}

resource "google_compute_instance" "db-instance" {
    name = "db-instance"
    machine_type = "custom-2-3072"
    zone = "us-east1-b"
    tags = ["db"]
    disk {
        image = "ubuntu-os-cloud/ubuntu-1604-lts"
        size = 100
    }
    network_interface {
        network = "squadster-private"
    }
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
        network = "squadster-private"
        access_config {
            // ephemeral public ip
        }
    }
}

resource "google_compute_http_health_check" "default" {
    name = "healthcheck"
    timeout_sec = 5
    check_interval_sec = 5
    port = "80"
}
