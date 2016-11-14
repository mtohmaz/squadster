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
  lat: null;
  lng: null;

  create: Event = {
    event_id: null,
    host_id: null,
    title: null,
    date: null,
    comments: null,
    max_attendees: null,
    description: null,
    location: null,
    lat: null,
    lng: null
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
        let lat = +params['lat'] || 0;
        let lng = +params['lng'] || 0;
        if (id != 0) {
          this.eventService.getEvent(id).then(ret => this.create = ret);
        }
      });
  }

  printLL(){
    console.log('lat is: ' + this.lat + ' lng is: ' + this.lng);
  }

  onFocus() {
    //let timer = Observable.timer(0, 3000);
    //timer.subscribe(t => this.getSuggestions());
    this._loader.load().then(() => {
      let autocomplete = new google.maps.places.Autocomplete(document.getElementById("google_places_ac"), {});
      google.maps.event.addListener(autocomplete, 'place_changed', () => {
        let place = autocomplete.getPlace();
        this.lat = place.geometry.location.lat();
        this.lng = place.geometry.location.lng();
        console.log('place is: ' + JSON.stringify(place.name) + ' lat/lng is: ' + this.lat + '/' + this.lng);
      });
    });
  }

   add(event: Event): void {
     if (!event) { return; }
     this.eventService.create(this.create.title, this.create.date, this.create.max_attendees, this.create.description, this.lat, this.lng)
                      .then(response => this.status = response);
   }

}
