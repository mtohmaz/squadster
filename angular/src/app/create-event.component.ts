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
  styleUrls: ['styles/create-event.component.css'],
  providers: [EventService]
})
export class CreateEventComponent {

  status: string;
  events: Event[];
  public minDate: Date = void 0;
  title = "Create a New Event";

  create: Event = {
    event_id: null,
    host_id: null,
    title: null,
    date: new Date(),
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
        this.create.lat = +params['lat'];
        this.create.lon = +params['lon'];
      }
      if (id != 0) {
        this.eventService.getEvent(id).then(ret => this.create = ret);
      }
    });
  }

  onFocus() {
    this._loader.load().then(() => {
      let autocomplete = new google.maps.places.Autocomplete(document.getElementById("google_places_ac"), {});
      google.maps.event.addListener(autocomplete, 'place_changed', () => {
        let place = autocomplete.getPlace();
        this.create.lat = parseFloat(place.geometry.location.lat().toFixed(7));
        this.create.lon = parseFloat(place.geometry.location.lng().toFixed(7));
      });
    });
  }

   add(event: Event): void {
     if (!event) { return; }

     this.eventService.create(this.create.title, this.create.date, this.create.max_attendees, this.create.description, this.create.location, this.create.lat, this.create.lon)
                      .then(response => this.status = response);
   }
}
