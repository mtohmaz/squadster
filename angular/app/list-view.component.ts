import { Component, OnInit } from '@angular/core';

import { Event } from './event';
import { EventService } from './event.service';
import { TopNavComponent } from './top-nav.component';

@Component({
  //moduleId: module.id,
  selector: 'list-view',
  templateUrl: 'app/html/list-view.component.html',
  styleUrls: ['app/styles/list-view.component.css'],
  providers: [EventService]
})

export class ListViewComponent implements OnInit {
  title = 'Events Nearby';
  events: Event[];
  selectedEvent: Event;

  constructor(private eventService: EventService) {
    let topNav = new TopNavComponent();
    console.log('value of isMapOn when in list-view is:' + topNav.isMapOn());
  }

  getEvents(): void {
    this.eventService.getEvents().then(events => this.events = events);
  }

  ngOnInit(): void {
    this.getEvents();
  }

  onSelect(event: Event): void {
    this.selectedEvent = event;
  }
}
