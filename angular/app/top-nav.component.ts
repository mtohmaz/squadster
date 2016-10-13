import {Component, ViewEncapsulation, OnInit} from "@angular/core";
//import {Routes} from "./../../config/route.config";
@Component({
    selector: "topnav",
    //templateUrl: "app/main/topNavbar/TopNavbar.html",
    template: `
      <div id="topnav">
        <div id="logo">
          <img src="../images/SquadsterLogo.png" />
        </div>
        <ul>
          <li><a routerLink="app/list-view" routerLinkActive="active">List View</a></li>
          <li><a routerLink="app/create-event" routerLinkActive="active">Create Event</a></li>
          <li><a routerLink="app/my-events" routerLinkActive="active">My Events</a></li>
          <li><a class="icon ion-person"> My Account </a> </li>
        </ul>
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
