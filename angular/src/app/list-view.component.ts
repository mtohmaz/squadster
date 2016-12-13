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

  totalItems:number;
  currentPage:number = 1;
  maxSize:number = 10;
  noEvents:boolean = false;

  lat: number;
  lon: number;
  location = {};
  range: number;
  s: string;

  title = 'List of Events';
  events: Event[];

  constructor(
    private eventService: EventService,
    private route: ActivatedRoute,
    private router: Router,
    private ref: ChangeDetectorRef
  ) { }

  joinEvent($event, e: Event): void {
    event.stopPropagation();
    this.eventService.joinEvent(e.event_id);
    this.getEvents(this.range, this.s);
  }

  getEvents(range: number, s: string): void {
    this.eventService.getEvents(this.lat, this.lon, range, s, this.currentPage).subscribe(response => {
      this.noEvents = response.count == 0 ? true : false;
      this.events = response.results;
      this.totalItems = response.count;
      this.ref.detectChanges();
    });
  }

  ngOnInit(): void {
    this.route.queryParams.forEach((params: Params) => {
      if (+params['lat'] && +params['lon']) {
        this.lat = +params['lat'];
        this.lon = +params['lon'];
        this.range = +params['radius'] || 1;
        this.currentPage = +params['page'] || 1;
        this.s = params['s'] || '';
        this.getEvents(this.range, this.s);
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

  pageChanged(event:any):void {
    this.currentPage = event.page;
    this.getEvents(this.range, this.s);
  }
}
