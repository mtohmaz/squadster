import { Component, OnInit } from '@angular/core';

import { Event } from './event';
import { EventService } from './event.service';

@Component({
  //moduleId: module.id,
  selector: 'list-view',
  template: `
    <h1>{{title}}</h1>
    <h2>Events</h2>
    <ul class="events">
      <li *ngFor="let event of events"
        [class.selected]="event === selectedEvent"
        (click)="onSelect(event)">
        <span class="badge">{{event.id}}</span> {{event.title}}
      </li>
    </ul>
    <my-event-detail [event]="selectedEvent"></my-event-detail>
  `,
  styleUrls: ['app/styles/list-view.component.css'],
  providers: [EventService]
})

export class ListViewComponent implements OnInit {
  title = 'Events Nearby';
  events: Event[];
  selectedEvent: Event;

  constructor(private eventService: EventService) { }

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
