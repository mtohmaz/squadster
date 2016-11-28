import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Event } from './event';
import { EventService } from './event.service';

@Component({
  selector: 'list-view',
  templateUrl: 'html/list-view.component.html',
  styleUrls: ['styles/list-view.component.css'],
  providers: [EventService]
})

export class ListViewComponent implements OnInit {

  lat: number;
  lon: number;
  location = {};

  title = 'Events Nearby';
  events: Event[];

  constructor(
    private eventService: EventService,
    private route: ActivatedRoute,
    private router: Router,
    private ref: ChangeDetectorRef
  ) { }

  getAllEvents(): void {
    this.eventService.getAllEvents().then(events => this.events = events);
  }

  getEvents(range: number, s: string): void {
    this.eventService.getEvents(this.lat, this.lon, range, s).then(events => {
      this.events = events;
      this.ref.detectChanges();
    });
  }

  ngOnInit(): void {
    this.route.queryParams.forEach((params: Params) => {
      //TO-DO need to check if lat and lon are passed.
      if (+params['lat'] && +params['lon']) {
        this.lat = +params['lat'];
        this.lon = +params['lon'];
        let range = +params['radius'] || 1;
        let s = params['s'] || '';
        this.getEvents(range, s);
      }
      else if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(this.setPosition.bind(this));
      }
    });
  }

  setPosition(position){
      this.location = position.coords;
      this.updateCurrentLatlon(position.coords.latitude, position.coords.longitude);
  }

  updateCurrentLatlon(latitude, longitude){
      this.lat = latitude;
      this.lon = longitude;
      this.getEvents(1, '');
  }

  onSelect(event: Event): void {
    this.router.navigate(['app/event-details'], { queryParams: { id: event.event_id }});
  }
}
