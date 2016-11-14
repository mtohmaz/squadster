import { Component, OnInit } from '@angular/core';
import { MouseEvent } from 'angular2-google-maps/core';
import { Router } from '@angular/router';

declare var google:any;

@Component({
    selector: 'map',
    templateUrl: 'html/map.component.html',
    styleUrls: ['styles/map.component.css'],
})

export class MapComponent implements OnInit{
    title: string = 'Events Nearby';
    lat: number = 50;
    lng: number = -50;
    zoom: number = 14;
    radius: number = 1609.34;
    circleColor: string = '#5DFC0A';
    newPinLat: number = null;
    newPinLng: number = null;

    //1 mile = 1609.34 meters
    mile = 1609.34;
    //radius: number = 20;
    location = {};
    distances = ['1 mile', '5 miles', '10 miles', '15 miles'];
    distanceSelected = this.distances[0];
    d_int = null;

    //TODO: take pre-populated events out and use events from the API
    //this should be replaced by events received from the API
    markers: marker[] = [
        {
            lat: 35.771673,
            lng: -78.673835,
            label: 'Coffee Hangout',
            iconUrl: 'assets/images/miniSLogo.png'
        },
        {
            lat: 35.779600,
            lng: -78.675779,
            label: 'Watch Doctor Strange',
            iconUrl: 'assets/images/miniSLogo.png'
        },
        {
            lat: 35.771238,
            lng: -78.674408,
            label: 'Pickup Frisby',
            iconUrl: 'assets/images/miniSLogo.png'
        }
    ];

    //when users click on the map, a new pin will be shown and added to this array to keep track of the info
    newPins: marker[] = [];

    constructor(
        private router: Router
    ) { }

    setPosition(position){
        this.location = position.coords;
        console.log(position.coords);
        this.updateCurrentLatLng(position.coords.latitude, position.coords.longitude);
    }

    updateCurrentLatLng(latitude, longitude){
        this.lat = latitude;
        this.lng = longitude;
    }

    ngOnInit(){
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(this.setPosition.bind(this));
        }
    }

    printLocation(){
        console.log('this.latitude is: ' + this.lat + '\nthis.longittude is: ' + this.lng);
        this.getAddress(this.lat, this.lng);
        console.log('distanceSelected selected: ' + this.distanceSelected);
    }

    mapClicked($event: MouseEvent) {
        this.newPins.push({
            lat: $event.coords.lat,
            lng: $event.coords.lng,
            iconUrl: 'assets/images/miniSLogo.png',
            label: ('Create event at: ' + $event.coords.lat + ', ' + $event.coords.lng)
        });
        this.getAddress($event.coords.lat, $event.coords.lng);
        this.newPinLat = $event.coords.lat;
        this.newPinLng = $event.coords.lng;
    }

    onChange(){
        this.d_int = parseInt(this.distanceSelected);
        this.radius = this.d_int * this.mile;
        if(this.d_int == 5){
            this.zoom = 12;
        }
        else if(this.d_int == 10){
            this.zoom = 11;
        }
        else if(this.d_int == 15){
            this.zoom = 10;
        }
        else{
            this.zoom = 14;
        }
    }

    getAddress(lat, lng){
        var geocoder = new google.maps.Geocoder();
        var latlng = new google.maps.LatLng(lat, lng);
        geocoder.geocode({ 'latLng': latlng }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[1]) {
                    console.log(results[1].formatted_address);
                } else {
                    console.log('Location not found');
                }
            } else {
                console.log('Geocoder failed due to: ' + status);
            }
        });
    }

    clickedMarker(marker: marker, index: number) {
        console.log(marker);
        console.log(`clicked the marker: ${marker.label || index}`);
    }

    dragEnd($event: MouseEvent){
        this.updateCurrentLatLng($event.coords.lat, $event.coords.lng);
        console.log('new position is: ' + $event.coords.lat + ', ' + $event.coords.lng);
        this.getAddress($event.coords.lat, $event.coords.lng);
    }

    host(lat: number, lng: number){
        console.log('marker lat: ' + lat + ' marker lng: ' + lng);
        this.router.navigate(['../app/create-event'], { queryParams: { lat: lat, lng: lng }});
    }

    //TODO: update query params with proper event ID's from the API
    eventDetails(lat: number, lng: number){
        console.log('marker lat: ' + lat + ' marker lng: ' + lng);
        this.router.navigate(['../app/event-details'], { queryParams: { lat: lat, lng: lng }});
    }
}

// just an interface for type safety.
interface marker {
    lat: number;
    lng: number;
    label?: string;
    iconUrl: string;
}
