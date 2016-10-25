import { Component } from '@angular/core';

@Component({
    selector: 'map',
    templateUrl: 'app/html/map.component.html',
    styleUrls: ['app/styles/map.component.css'],
})
export class MapComponent {
    title: string = 'Events Nearby';
    lat: number = 35.771700;
    lng: number = -78.673564;
    zoom: number = 17;
}