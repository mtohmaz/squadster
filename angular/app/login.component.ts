import { Component } from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'login',
  template: `
    <h1>{{title}}</h1>
    <img src="../images/SquadsterLogo.png" alt="Squadster">
    <div class="row">
        <div class="col-xs-2">
            Email: <input type="text">
        </div>
    </div>
    <div class="row">
        <div class="col-xs-2">
            Password: <input type="text">
        </div>
    </div>
    <button (click)="login()"> Login </button>
  `
})

export class LoginComponent {
  loggedIn: boolean = false;

  constructor(
      private router: Router
  ){}

  login() {
    this.loggedIn = !this.loggedIn;
    this.router.navigate(['app/list-view']);
  }
}