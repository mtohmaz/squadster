import { Component, ViewEncapsulation, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { DropdownModule } from "ng2-bootstrap/ng2-bootstrap";
import { Headers, Http, Response } from '@angular/http';

@Component({
    selector: 'searchbar',
    templateUrl: 'html/search-bar.component.html',
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['styles/search-bar.component.css'],
})

export class SearchBarComponent {

    public status:{isopen:boolean} = {isopen: false};
    lat: number;
    lng: number;
    location = {};
    distances = [1, 5, 10, 15, 25];
    tags = ['Food', 'Gaming', 'Hangout', 'Movie', 'Sports', 'Study'];
    locations = ['Current Location', 'Raleigh, NC', 'Cary, NC', 'Durham, NC', 'Chapel Hill, NC'];
    distanceSelected = this.distances[0];
    tagSelected = null;
    locationSelected = this.locations[0];
    searchString = '';

    constructor(
      private router: Router
    ) { }

    ngOnInit(){
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(this.setPosition.bind(this));
        }
    }

    setPosition(position){
        this.location = position.coords;
        console.log(position.coords);
        this.updateCurrentLatLng(position.coords.latitude, position.coords.longitude);
    }

    updateCurrentLatLng(latitude, longitude){
        this.lat = latitude;
        this.lng = longitude;
    }

    updateSearch( search: string ) {
      if (this.router.url.indexOf("app/map-view") !== -1) {
        if (search) {
          this.router.navigate(['app/map-view'], { queryParams: { s: search, radius: this.distanceSelected, lat: this.lat, lon: this.lng}});
        }
        else {
          this.router.navigate(['app/map-view'], { queryParams: { radius: this.distanceSelected, lat: this.lat, lon: this.lng}});
        }
      }
      else {
        if (search) {
          this.router.navigate(['app/list-view'], { queryParams: { s: search, radius: this.distanceSelected, lat: this.lat, lon: this.lng}});
        }
        else {
          this.router.navigate(['app/list-view'], { queryParams: { radius: this.distanceSelected, lat: this.lat, lon: this.lng}});
        }
      }
    }
    /*
    public doLogout():void {
        console.log('made it to doLogout');
        return this.http
               .delete('http://localhost/api/auth/', null, {headers: this.headers})
               .toPromise()
               .then(response => console.log(response.json()))
               .catch(this.handleError);
    }
    */
    updateTag( tag ){
        this.tagSelected = tag;
    }
}
