import { Component, ViewEncapsulation, OnInit } from "@angular/core";
//import {Routes} from "./../../config/route.config";
@Component({
    selector: "topnav",
    //templateUrl: "app/main/topNavbar/TopNavbar.html",
    templateUrl: 'html/top-nav.component.html',
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['styles/top-nav.component.css', 'styles/mapswitch.css'],
})

/*export class TopNavbarComponent  {
    showNavBar: boolean = false;


    constructor(private globalEventsManager: GlobalEventsManager) {
        this.globalEventsManager.showNavBar.subscribe((mode)=>{
            this.showNavBar = mode;
        });

    }


}*/

export class TopNavComponent {
    private mapOn: boolean = true;

    toggle() {
        this.mapOn = (this.mapOn) ? false : true;
        console.log('mapOn value is ' + this.mapOn);
    }

    isMapOn() : boolean{
        return this.mapOn;
    }
}
