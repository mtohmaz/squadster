import {Component} from '@angular/core'; //calls the decorater core component.
//import {CreateService} from './create.service';

export class Create {
  title: string;
  location: string;
  startDate: Date;
  startTime: Date;
  endDate: Date;
  endTime: Date;
  maxAttendees: number;
  description: string;
}

@Component({ //tells angular that this file is a component.
  selector: 'create',
  template: `
  <h2>{{ title }}</h2>
  <div>
    <label>Event Title: </label>
    <input [(ngModel)]="create.title">
    <br><br>

    <label>Event Location: </label>
    <input [(ngModel)]="create.location">
    <br><br>

    <label>Start Date: </label>
    <datepicker [(ngModel)]="create.startDate" [showWeeks]="false"></datepicker>

    <label>&nbsp; Start Time: </label>
    <input type="time" [(ngModel)]="create.startTime">
    <br><br>

    <label>End Date: </label>
    <datepicker [(ngModel)]="create.endDate" [showWeeks]="false"></datepicker>

    <label>&nbsp; End Time: </label>
    <input type="time" [(ngModel)]="create.endTime">
    <br><br>

    <label>Max Attendees: </label>
    <input [(ngModel)]="create.maxAttendees">
    <br><br>

    <label>Description: </label>
    <input [(ngModel)]="create.description">
  </div>
  `/*,
  providers: [CreateService]*/
})
export class CreateComponent {
  title = "Create Event";
  create: Create = {
    title: null,
    location: null,
    startDate: null,
    startTime: null,
    endDate: null,
    endTime: null,
    maxAttendees: null,
    description: null
  };

/*  constructor(createService: CreateService) {
    this.create = createService.getCreate();
  }
*/
}
