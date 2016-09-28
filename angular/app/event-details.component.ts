import { Component, Input } from '@angular/core';
import { Event } from './event';

@Component({
  selector: 'my-event-detail',
  template: `
    <div *ngIf="event">
      <h2>{{event.title}} details:</h2>
      <div>
        <label>Name of Event:</label> {{event.title}}
      </div>
      <div>
        <label>Location:</label> {{event.location}}
      </div>
      <div>
        <label>Description:</label> {{event.description}}
      </div>
      <div>
        <label>Date:</label> {{event.startDate}}
      </div>
      <div>
        <label>Time:</label> {{event.startTime}}
      </div>
      <div>
        <label>Attendees so far:</label> {{event.currentAttendees}}/{{event.maxAttendees}}
      </div>
    </div>
  `
})

export class EventDetailComponent {
  @Input() event: Event;
}
