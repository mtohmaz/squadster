import { Component, OnInit } from '@angular/core';

@Component({
    selector: 'map',
    templateUrl: 'app/html/map.component.html',
    styleUrls: ['app/styles/map.component.css'],
})
export class MapComponent implements OnInit{
    title: string = 'Events Nearby';
    lat: number = 35.771700;
    lng: number = -78.673564;
    zoom: number = 17;

    ngOnInit(){
        if(navigator.geolocation){
            console.log('made it inside geolocation');

            navigator.geolocation.getCurrentPosition(function(position) {
                    this.lat= position.coords.latitude,
                    this.lng= position.coords.longitude
            });
        }
        console.log('latitude is: ' + this.lat + '\nlongittude is: ' + this.lng);
    }
}