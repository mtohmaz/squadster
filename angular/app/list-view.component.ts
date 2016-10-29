import { Component, OnInit, Output, EventEmitter } from '@angular/core';

import { Event } from './event';
import { EventService } from './event.service';

@Component({
  //moduleId: module.id,
  selector: 'list-view',
  templateUrl: 'app/html/list-view.component.html',
  styleUrls: ['app/styles/list-view.component.css'],
  providers: [EventService]
})

export class ListViewComponent implements OnInit {
  @Output() isMap = new EventEmitter<boolean>();

  title = 'Events Nearby';
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
