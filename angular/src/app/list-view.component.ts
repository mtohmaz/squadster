import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Event } from './event';
import { EventService } from './event.service';

@Component({
  //moduleId: module.id,
  selector: 'list-view',
  templateUrl: 'html/list-view.component.html',
  styleUrls: ['styles/list-view.component.css'],
  providers: [EventService]
})

export class ListViewComponent implements OnInit {
  @Output() isMap = new EventEmitter<boolean>();

  lat: number;
  lon: number;
  location = {};

  title = 'Events Nearby';
  events: Event[];
  //selectedEvent: Event;

  constructor(
    private eventService: EventService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  getAllEvents(): void {
    this.eventService.getAllEvents().then(events => this.events = events);
  }

  ngOnInit(): void {
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(this.setPosition.bind(this));
    }
    //param : string[];
    //param.push("test");

  }

  getEvents() {
    this.route.queryParams.forEach((params: Params) => {
      console.log(this.lat);
      let lat = +params['lat'] || this.lat;
      console.log(lat);
      let lon = +params['lon'] || this.lon;
      let range = +params['radius'] || 1;
      let s = params['s'] || '';
      this.eventService.getEvents(lat, lon, range, s).then(events => this.events = events);
    });
  }

  setPosition(position){
      this.location = position.coords;
      console.log(position.coords);
      this.updateCurrentLatlon(position.coords.latitude, position.coords.longitude);
  }

  updateCurrentLatlon(latitude, longitude){
      this.lat = latitude;
      this.lon = longitude;
      this.getEvents();
  }

  onSelect(event: Event): void {
    this.router.navigate(['app/event-details'], { queryParams: { id: event.event_id }});
  }
}
