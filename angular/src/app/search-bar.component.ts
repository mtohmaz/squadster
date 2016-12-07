import { Component, ViewEncapsulation, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { DropdownModule } from "ng2-bootstrap/ng2-bootstrap";
import { Headers, Http, Response } from '@angular/http';
import { MapsAPILoader } from 'angular2-google-maps/core';
import { NotificationsService } from 'angular2-notifications';

declare var google:any;

@Component({
    selector: 'searchbar',
    templateUrl: 'html/search-bar.component.html',
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['styles/search-bar.component.css'],
})

export class SearchBarComponent {

    public status:{isopen:boolean} = {isopen: false};
    lat: number;
    lon: number;
    location = {};
    distances = [1, 5, 10, 15, 25];
    tags = ['Food', 'Gaming', 'Hangout', 'Movie', 'Sports', 'Study'];
    distanceSelected = this.distances[0];
    tagSelected = null;
    locationSelected = "Current location";
    searchString = '';
    private headers = new Headers({'Content-Type': 'application/json'});

    public options = {
        timeOut: 5000,
        lastOnBottom: true,
        clickToClose: true,
        maxLength: 0,
        maxStack: 7,
        showProgressBar: true,
        pauseOnHover: true,
        preventDuplicates: false,
        preventLastDuplicates: 'visible',
        rtl: false,
        animate: 'scale',
        position: ['right', 'bottom']
    };

    constructor(
      private router: Router,
      private _loader: MapsAPILoader,
      private _service: NotificationsService,
      private http: Http
    ) { }

    ngOnInit() {
        if(navigator.geolocation && !this.lat && !this.lon){
            navigator.geolocation.getCurrentPosition(this.setPosition.bind(this));
        }
    }

    checkToggle() {
      if (this.locationSelected != "Current Location") {
        (<HTMLAnchorElement>document.getElementById("createicon")).className = "icon ion-navigate";
      }
      else {
        (<HTMLAnchorElement>document.getElementById("createicon")).className = "icon ion-navigate active";
        if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition(this.setPosition.bind(this));
        }
      }
    }

    clickNav() {
      this.locationSelected = "Current Location";
      this.checkToggle();
      let input = (<HTMLInputElement>document.getElementById("box")).value;
      this.updateSearch(input)
    }

    findLocation() {
      this.checkToggle();
      this._loader.load().then(() => {
        let autocomplete = new google.maps.places.Autocomplete(document.getElementById("location"), {});
        google.maps.event.addListener(autocomplete, 'place_changed', () => {
          let place = autocomplete.getPlace();
          if (!place.geometry) {
            this._service.error("Location Not Found", "Please select a valid location");
            return;
          }
          this.lat = place.geometry.location.lat();
          this.lon = place.geometry.location.lng();
          let input = (<HTMLInputElement>document.getElementById("box")).value;
          this.updateSearch(input);
        });
      });
    }

    setPosition(position){
        this.location = position.coords;
        this.updateCurrentLatlon(position.coords.latitude, position.coords.longitude);
    }

    updateCurrentLatlon(latitude, longitude){
        this.lat = latitude;
        this.lon = longitude;
        let input = (<HTMLInputElement>document.getElementById("box")).value;
        if (this.router.url.indexOf("app/map-view") !== -1 ||
            this.router.url.indexOf("app/list-view") !== -1) {
              this.updateSearch(input);
            }
    }

    updateSearch( search: string ) {
      if (this.router.url.indexOf("app/map-view") !== -1) {
        if (search) {
          this.router.navigate(['app/map-view'], { queryParams: { s: search, radius: this.distanceSelected, lat: this.lat, lon: this.lon}});
        }
        else {
          this.router.navigate(['app/map-view'], { queryParams: { radius: this.distanceSelected, lat: this.lat, lon: this.lon}});
        }
      }
      else {
        if (search) {
          this.router.navigate(['app/list-view'], { queryParams: { s: search, radius: this.distanceSelected, lat: this.lat, lon: this.lon}});
        }
        else {
          this.router.navigate(['app/list-view'], { queryParams: { radius: this.distanceSelected, lat: this.lat, lon: this.lon}});
        }
      }
    }

    doLogout(): Promise<any> {
        console.log('made it to doLogout');
        return this.http.delete('/api/auth/', {headers: this.headers})
              .toPromise()
              .then(response => console.log(response.json()))
              .catch(this.handleError);
    }

    updateTag( tag ){
        this.tagSelected = tag;
    }

    private handleError(error: any): Promise<any> {
      if (error.status == 400)
        return Promise.resolve("Bad Request");
      else if (error.status == 401)
        return Promise.resolve("Not logged in");
      else if (error.status == 403)
        return Promise.resolve("Not authenticated");
      else
        return Promise.reject(error.message || error);
    }
}
