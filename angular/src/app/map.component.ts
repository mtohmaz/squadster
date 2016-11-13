import { Component, OnInit, NgModule } from '@angular/core';
import { AgmCoreModule } from 'angular2-google-maps/core';
import { BrowserModule } from '@angular/platform-browser';

@Component({
    selector: 'map',
    templateUrl: 'html/map.component.html',
    styleUrls: ['styles/map.component.css'],
})

export class MapComponent implements OnInit{
    title: string = 'Events Nearby';
    lat: number = 50;
    lng: number = -50;
    zoom: number = 17;
    location = {};

    markers: marker[] = [
        {
            lat: 35.771673,
            lng: -78.673835,
            label: 'Coffee Hangout',
            draggable: false,
            iconUrl: 'http://i.imgur.com/4HFujqP.png'
        },
        {
            lat: 35.779600,
            lng: -78.675779,
            label: 'Watch Doctor Strange',
            draggable: false,
            iconUrl: 'http://i.imgur.com/4HFujqP.png'
        },
        {
            lat: 35.771238,
            lng: -78.674408,
            label: 'Pickup Frisby',
            draggable: false,
            iconUrl: 'http://i.imgur.com/4HFujqP.png'
        }
    ]

    setPosition(position){
        this.location = position.coords;
        console.log(position.coords);
        this.lat = position.coords.latitude;
        this.lng = position.coords.longitude;
    }

    ngOnInit(){
        if(navigator.geolocation){
            console.log('made it inside geolocation');

            navigator.geolocation.getCurrentPosition(this.setPosition.bind(this));
        }
        console.log('this.latitude is: ' + this.lat + '\nthis.longittude is: ' + this.lng);
    }

    printLocation(){
        console.log('this.latitude is: ' + this.lat + '\nthis.longittude is: ' + this.lng);
    }

    mapClicked($event: MouseEvent) {
        // this.markers.push({
          //   lat: $event.,
            // lng: $event.coords.lng
         //});
        console.log($event);
    }
}

// just an interface for type safety.
interface marker {
    lat: number;
    lng: number;
    label?: string;
    draggable: boolean;
    iconUrl: string;
}
