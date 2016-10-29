import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
//import {CreateComponent} from './create.component';

@Component({
    selector: 'my-app',
    template: `
    <div id="head">
      <div id="nav">
        <searchbar></searchbar>
        <topnav></topnav>
      </div>
      <div class="col-xs-2" id="filter">
        <filters></filters>
      </div>
      <div class="col-xs-1"></div>
      <div id="body" class="col-xs-6">
        <router-outlet></router-outlet>
      </div>
      <div class="col-xs-3">
        <a routerLink="app/create-event" routerLinkActive="active" id="createicon" class="icon ion-plus-circled" title="Host a new event"></a>
      </div>
    </div>
    <div *ngIf="isEdited()" class="col-xs-3 margin">
        <div class="mapswitch">
            <input type="checkbox" name="mapswitch" class="mapswitch-checkbox" id="mymapswitch" [checked]="check()" (change)="toggle()">
            <label class="mapswitch-label" for="mymapswitch">
                <span class="mapswitch-inner"></span>
                <span class="mapswitch-switch"></span>
            </label>
        </div>
    </div>

    `,
    styleUrls: ['app/styles/master-styles.css', 'app/styles/mapswitch.css'],
    //state which components are used in the template.
    //directives: [CreateComponent]
})
export class AppComponent {
    private _open: boolean = false;
    isChecked = false;

    constructor(public router: Router) { }

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
