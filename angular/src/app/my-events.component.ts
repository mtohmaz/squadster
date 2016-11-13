import { Component } from '@angular/core';
import { Event } from './event';
import { EventService } from './event.service';

@Component({
  selector: 'my-events',
  template: `
    <h1>{{title}}</h1>
    <h2>My Events</h2>
    <ul class="events">
      <li *ngFor="let event of events"
        [class.selected]="event === selectedEvent"
        (click)="onSelect(event)">
        <span class="badge">{{event.id}}</span> {{event.title}}
      </li>
    </ul>
    <myEventDetail [event]="selectedEvent"></myEventDetail>
  `,
  styleUrls: ['styles/my-events.component.css'],
  providers: [EventService]
})
export class MyEventsComponent {
  title = 'My Events';
  events: Event[];
  selectedEvent: Event;

  constructor(private eventService: EventService) { }

  getAllEvents(): void {
    this.eventService.getAllEvents().then(events => this.events = events);
  }

  ngOnInit(): void {
    this.getAllEvents();
  }

  onSelect(event: Event): void {
    this.selectedEvent = event;
  }
}
