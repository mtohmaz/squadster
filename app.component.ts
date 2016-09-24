import { Component } from '@angular/core';

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

@Component({
    selector: 'my-app',
    template: `
    <h1>{{title}}</h1>
    <!-- <h2>{{create.name}} details!</h2>
    <div><label>id: </label>{{create.id}}</div> -->
    <div>
      <label>Event Title: </label>
      <input [(ngModel)]="create.title">
      <br><br>

      <label>Event Location: </label>
      <input [(ngModel)]="create.location">
      <br><br>

      <label>Start Date: </label>
      <input type="date" [(ngModel)]="create.startDate">

      <label>&nbsp; Start Time: </label>
      <input type="time" [(ngModel)]="create.startTime">
      <br><br>

      <label>End Date: </label>
      <input type="date" [(ngModel)]="create.endDate">

      <label>&nbsp; End Time: </label>
      <input type="time" [(ngModel)]="create.endTime">
      <br><br>

      <label>Max Attendees: </label>
      <input [(ngModel)]="create.maxAttendees">
      <br><br>

      <label>Description: </label>
      <input [(ngModel)]="create.description">
    </div>
    `
})
export class AppComponent {
    title = 'Create Event';
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
}
