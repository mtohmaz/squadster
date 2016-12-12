import { Component, ChangeDetectorRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { Event } from './event';
import { EventService } from './event.service';

@Component({
  selector: 'my-events',
  templateUrl: 'html/my-events.component.html',
  styleUrls: ['styles/my-events.component.css'],
  providers: [EventService]
})
export class MyEventsComponent {
  attendTitle = 'Events I\'m Attending';
  hostTitle = 'Events I\'m Hosting';
  attended: Event[];
  hosted: Event[];
  noAttendedEvents:boolean = false;
  noHostedEvents:boolean = false;
  selectedEvent: Event;

  totalAttendItems:number;
  totalHostItems:number;
  currentAttendPage:number = 1;
  currentHostPage:number = 1;
  userId:number;
  maxSize:number = 10;

  constructor(
    private eventService: EventService,
    private route: ActivatedRoute,
    private router: Router,
    private ref: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.getCurrentUserId();
    this.getAttendedEvents();
    this.getHostedEvents();
  }

  getCurrentUserId(){
    this.eventService.getCurrentUserId().subscribe(response => {
      this.userId = JSON.parse(response.id);
      this.ref.detectChanges();
    });
  }

  getAttendedEvents(){
    this.eventService.getAttendedEvents(this.userId, this.currentAttendPage).subscribe(response => {
      this.noAttendedEvents = response.count == 0 ? true : false;
      this.attended = response.results;
      this.totalAttendItems = response.count;
      this.ref.detectChanges();
    });
  }

  getHostedEvents(){
    this.eventService.getHostedEvents(this.userId, this.currentHostPage).subscribe(response => {
      this.noHostedEvents = response.count == 0 ? true : false;
      this.hosted = response.results;
      this.totalHostItems = response.count;
      this.ref.detectChanges();
    });
  }

  onSelect(event: Event): void {
    this.selectedEvent = event;
  }

  attendedPageChanged(event:any):void {
    this.currentAttendPage = event.page;
    this.getAttendedEvents();
  }

  hostedPageChanged(event:any):void {
    this.currentHostPage = event.page;
    this.getHostedEvents();
  }
}
