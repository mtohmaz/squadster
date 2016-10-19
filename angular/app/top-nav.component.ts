import {Component, ViewEncapsulation, OnInit} from "@angular/core";
//import {Routes} from "./../../config/route.config";
@Component({
    selector: "topnav",
    //templateUrl: "app/main/topNavbar/TopNavbar.html",
    template: `
    <div class="row">
      <div id="topnav">
        <div class="col-xs-3 element">
            <a routerLink="app/list-view" routerLinkActive="active">List View</a>
        </div>
        <div class="col-xs-3 element">
            <a routerLink="app/create-event" routerLinkActive="active">Create Event</a>
        </div>
        <div class="col-xs-3 element">
            <a routerLink="app/my-events" routerLinkActive="active">My Events</a>
        </div>
        <div class="col-xs-3 element">
            <a routerLink="app/login" routerLinkActive="active" class="icon ion-person"> My Account </a>
        </div>
      </div>
    </div>
    `,
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['app/styles/top-nav.component.css'],
})

/*export class TopNavbarComponent  {
    showNavBar: boolean = false;


    constructor(private globalEventsManager: GlobalEventsManager) {
        this.globalEventsManager.showNavBar.subscribe((mode)=>{
            this.showNavBar = mode;
        });

    }


}*/

export class TopNavComponent { }
