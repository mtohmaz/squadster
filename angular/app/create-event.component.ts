import {Component} from '@angular/core'; //calls the decorater core component.
//import {CreateService} from './create.service';

export class Create {
  title: string;
  location: string;
  eventDate: Date;
  eventTime: Date;
  maxAttendees: number;
  description: string;
}

@Component({ //tells angular that this file is a component.
  selector: 'create-event',
  template: `
  <h2>{{ title }}</h2>
  <div class="body">
    <label>Event Title: </label>
    <input [(ngModel)]="create.title">
    <br><br>

    <label>Event Location: </label>
    <input [(ngModel)]="create.location">
    <br><br>

    <label>Date: </label>
    <datepicker [(ngModel)]="create.eventDate" [showWeeks]="false"></datepicker>

    <label>&nbsp;Time: </label>
    <input type="time" [(ngModel)]="create.eventTime">
    <br><br>

    <label>Max Attendees: </label>
    <input [(ngModel)]="create.maxAttendees">
    <br><br>

    <label>Description: </label>
    <input [(ngModel)]="create.description">
  </div>
  `,
  styleUrls: ['app/styles/master-styles.css'],/*,
  providers: [CreateService]*/
})
export class CreateEventComponent {
  title = "Create Event";
  create: Create = {
    title: null,
    location: null,
    eventDate: null,
    eventTime: null,
    maxAttendees: null,
    description: null
  };

/*  constructor(createService: CreateService) {
    this.create = createService.getCreate();
  }
*/
}
