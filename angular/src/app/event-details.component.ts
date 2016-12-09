import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Event } from './event';
import { EventService } from './event.service';
import { Comment } from './comment';

@Component({
  selector: 'event-details',
  templateUrl: 'html/event-details.component.html',
  styleUrls: ['styles/event-details.component.css'],
  providers: [EventService]
})

export class EventDetailsComponent {
  event: Event;
  comments: Comment[] = [];
  inputComment: string;
  event_id: number;

  totalItems:number;
  totalPages:number;
  maxSize:number = 10;
  pageCount:number = 1;
  noMoreComments:boolean = false;

  lat:number;
  lon:number;
  zoom:number = 17;
  iconUrl:string = 'assets/images/miniSLogo.png';

  constructor(
    private router: ActivatedRoute,
    private eventService: EventService,
    private ref: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.getEvent();
    this.getComments();
  }

  getEvent() {
    this.router.queryParams.forEach((params: Params) => {
      this.event_id = +params['id'] || 0;
      if (this.event_id != 0) {
        this.eventService.getEvent(this.event_id).then(response => {
          this.event = response;
          this.event.coordinates = this.event.coordinates.replace('[', '');
          this.event.coordinates = this.event.coordinates.replace(']', '');
          let latlon = this.event.coordinates.replace(',', '').split(" ");
          this.lat = parseFloat(latlon[0]);
          this.lon = parseFloat(latlon[1]);
          this.ref.detectChanges();
        });
      }
    });
  }

  getComments(){
    this.eventService.getComments(this.event_id, this.pageCount).subscribe(response => {
      if( response.results.length == 0 ){
        this.noMoreComments = true;
        return;
      }
      else{
        this.comments = this.comments.concat(response.results);
        this.totalItems = response.count;
        this.totalPages = Math.ceil( this.totalItems/this.maxSize );
        if( this.pageCount == this.totalPages){
          this.noMoreComments = true;
        }
        this.ref.detectChanges();
      }
    });
  }

  //hides show more text if no more comments to show
  getMoreComments(){
    if( this.pageCount < this.totalPages ){
      this.pageCount++;
      this.getComments();
    }
    else{
      this.noMoreComments = true;
    }
  }

  addComment() {
    this.eventService.addComment(this.event.comments, this.inputComment).then(response => {this.comments = [];this.getComments()});
    this.inputComment = '';
  }
}
