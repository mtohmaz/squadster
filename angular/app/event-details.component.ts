import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Event } from './event';

@Component({
  selector: 'my-event-detail',
  template: `
    <div *ngIf="event">
      <h2>{{event.title}} details:</h2>
      <div>
        <label>Event ID:</label> {{event.event_id}}
      </div>
      <div>
        <label>Name of Event:</label> {{event.title}}
      </div>
      <div>
        <label>Host Name:</label> {{event.host_id}}
      </div>
      <div>
        <label>Location:</label> {{event.location}}
      </div>
      <div>
        <label>Description:</label> {{event.description}}
      </div>
      <div>
        <label>Date:</label> {{event.date}}
      </div>
      <div>
        <label>Time:</label> {{event.startTime}}
      </div>
      <div>
        <label>Attendees so far:</label> {{event.currentAttendees}}/{{event.maxAttendees}}
      </div>
      <div>
        <label>Max Attendees:</label> {{event.max_attendees}}
      </div>
      <button (click)="onClick(event)">View Details</button>
    </div>
  `
})

export class EventDetailComponent {
  @Input() event: Event;

  constructor( private router: Router) {}

  onClick() {
    this.router.navigate(['app/create-event'], { queryParams: { id: this.event.event_id }});
  }
}
