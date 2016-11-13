import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
declare var google: any;
//import {CreateComponent} from './create.component';

@Component({
    selector: 'my-app',
    templateUrl: 'html/app.component.html',
    styleUrls: ['styles/master-styles.css', 'styles/mapswitch.css'],
    //state which components are used in the template.
    //directives: [CreateComponent]
})
export class AppComponent {
    private _open: boolean = false;
    isChecked = false;

    constructor(public router: Router) { }

    ngOnInit() {
      var map = {
        center: new google.maps.LatLng(51, -.12),
        zoom: 5,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };
    }
    isEdited() {
      if (this.router.url == "/app/list-view" || this.router.url == "/app/map-view")
        return true;
      return false;
    }

    check() {
        if (this.router.url == "/app/list-view") {
          this.isChecked = false;
        }
        else if (this.router.url == "app/map-view") {
          this.isChecked = true;
        }
        return this.isChecked;
    }

    toggle() {
        if (this.router.url == "/app/list-view") {
          this.router.navigate(["app/map-view"]);
        }
        else {
          this.router.navigate(["app/list-view"]);
        }
    }

    private _toggleSidebar() {
        this._open = !this._open;
    }
}
