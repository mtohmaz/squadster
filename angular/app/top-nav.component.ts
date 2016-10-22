import {Component, ViewEncapsulation, OnInit} from "@angular/core";
//import {Routes} from "./../../config/route.config";
@Component({
    selector: "topnav",
    //templateUrl: "app/main/topNavbar/TopNavbar.html",
    template: `
    <div class="row">
      <div id="topnav">
        <div class="col-xs-1">
        </div>
        <div class="col-xs-2 margin">
            <button type="button" class="btn btn-info btn-block" routerLink="app/list-view" routerLinkActive="active">Events Nearby</button>
        </div>
        <div class="col-xs-2 margin">
            <button type="button" class="btn btn-info btn-block" routerLink="app/my-events" routerLinkActive="active">My Events</button>
        </div>
        <div class="col-xs-3">
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
