import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
//import {CreateComponent} from './create.component';

@Component({
    selector: 'my-app',
    templateUrl: 'html/app.component.html',
    styleUrls: ['styles/master-styles.css', 'styles/mapswitch.css'],
    //state which components are used in the template.
    //directives: [CreateComponent]
})
export class AppComponent implements OnInit{
    private _open: boolean = false;
    isChecked = false;

    constructor(public router: Router) { }

    ngOnInit() {
      this.check();
    }

    isEdited() {
      if (this.router.url.search("/app/list-view") == 0 || this.router.url.search("/app/map-view") == 0)
        return true;
      return false;
    }

    check() {
        if (this.router.url.search("/app/list-view") == 0) {
          this.isChecked = false;
        }
        else if (this.router.url.search("app/map-view") == 0) {
          this.isChecked = true;
        }
        return this.isChecked;
    }

    toggle() {
      if (this.router.url.search("/app/list-view") == 0) {
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
