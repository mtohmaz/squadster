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

  ngOnInit(): void {
    this.route.queryParams.forEach((params: Params) => {
      //TO-DO need to check if lat and lon are passed.
      let lat = +params['lat'] || this.lat;
      let lon = +params['lon'] || this.lon;
      let range = +params['radius'] || 1;
      let s = params['s'] || '';
      this.eventService.getEvents(lat, lon, range, s).then(events => {
        this.events = events;
        this.ref.detectChanges();
      });
    });
  }

  onSelect(event: Event): void {
    this.router.navigate(['app/event-details'], { queryParams: { id: event.event_id }});
  }
}
