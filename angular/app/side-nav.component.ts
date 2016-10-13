import {Component, ViewEncapsulation, OnInit} from "@angular/core";
//import {Routes} from "./../../config/route.config";
@Component({
    selector: "sidenav",
    //templateUrl: "app/main/topNavbar/TopNavbar.html",
    template: `
      <div id="sidenav">
        <ul>
          <li><a routerLink="app/list-view" routerLinkActive="active">List View</a></li>
          <li><a routerLink="app/create-event" routerLinkActive="active">Create Event</a></li>
          <li><a routerLink="app/my-events" routerLinkActive="active">My Events</a></li>
        </ul>
      </div>
    `,
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['app/styles/side-nav.component.css'],
})

/*export class TopNavbarComponent  {
    showNavBar: boolean = false;


    constructor(private globalEventsManager: GlobalEventsManager) {
        this.globalEventsManager.showNavBar.subscribe((mode)=>{
            this.showNavBar = mode;
        });

    }


}*/

export class SideNavComponent { }
