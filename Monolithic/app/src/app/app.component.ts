import { Component ,ChangeDetectionStrategy,ChangeDetectorRef } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { HttpHeaders } from '@angular/common/http';
import {  Router  } from '@angular/router';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  changeDetection : ChangeDetectionStrategy.Default
})
export class AppComponent {
  showLoadingIndicator;
  status;
  constructor(private router: Router,private http: HttpClient,private cd: ChangeDetectorRef) {

  }
  title = 'app';
  headers = new HttpHeaders({'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'});
  onClick1() {
    this.showLoadingIndicator = true;
    
    this.http.get("http://127.0.0.1:5000/gmail").subscribe(
      res => {
        
        this.showLoadingIndicator = false;
        console.log("callback:"+res)
        this.router.navigate(['/all']);
        return res;
        
      },
      error  => {
  
        console.log("Error", error);
        
        }
    );

    
  }

  onClick2() {
    this.showLoadingIndicator = true;
    
    this.http.get("http://127.0.0.1:5000/outlook").subscribe(
      res => {
        
        this.showLoadingIndicator = false;
        console.log("callback:"+res)
        this.router.navigate(['/all']);
        return res;
        
      },
      error  => {
  
        console.log("Error", error);
        
        }
    );

    
  }




}
