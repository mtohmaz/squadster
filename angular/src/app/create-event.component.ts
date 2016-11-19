import { Component } from '@angular/core';
import * as moment from 'moment';
import { ActivatedRoute, Params } from '@angular/router';
import { Observable } from 'rxjs/Rx';
import { MapsAPILoader } from 'angular2-google-maps/core';

import { Event } from './event';
import { EventService } from './event.service';

declare var google:any;

@Component({ //tells angular that this file is a component.
  selector: 'create-event',
  templateUrl: 'html/create-event.component.html',
  styleUrls: ['styles/master-styles.css'],
  providers: [EventService]
})
export class CreateEventComponent {

  status: string;
  events: Event[];
  public minDate: Date = void 0;
  title = "Create Event";
  inputValue: string;
  lat: number;
  lon: number;

  create: Event = {
    event_id: null,
    host_id: null,
    title: null,
    date: null,
    comments: null,
    coordinates: null,
    max_attendees: null,
    description: null,
    location: null,
    lat: null,
    lon: null
  };

  constructor (
      private eventService: EventService,
      private route: ActivatedRoute,
      private _loader: MapsAPILoader )
  {
    (this.minDate = new Date()).setDate(this.minDate.getDate());
  }

  ngOnInit() {
    this.route.queryParams.forEach((params: Params) => {
      let id = +params['id'] || 0;
      if (params['lat']) {
        this.lat = +params['lat'];
        this.lon = +params['lon'];
      }
      if (id != 0) {
        this.eventService.getEvent(id).then(ret => this.create = ret);
      }
    });
  }

  printLL(){
    console.log('lat is: ' + this.lat + ' lon is: ' + this.lon);
  }

  onFocus() {
    //let timer = Observable.timer(0, 3000);
    //timer.subscribe(t => this.getSuggestions());
    this._loader.load().then(() => {
      let autocomplete = new google.maps.places.Autocomplete(document.getElementById("google_places_ac"), {});
      google.maps.event.addListener(autocomplete, 'place_changed', () => {
        let place = autocomplete.getPlace();
        this.lat = place.geometry.location.lat();
        this.lon = place.geometry.location.lon();
        console.log('place is: ' + JSON.stringify(place.name) + ' lat/lon is: ' + this.lat + '/' + this.lon);
      });
    });
  }

   add(event: Event): void {
     if (!event) { return; }
     this.eventService.create(this.create.title, this.create.date, this.create.max_attendees, this.create.description, this.create.location, parseFloat(this.lat.toFixed(7)), parseFloat(this.lon.toFixed(7)))
                      .then(response => this.status = response);
   }
}
