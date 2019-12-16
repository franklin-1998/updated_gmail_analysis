import { Injectable } from '@angular/core';
import { HttpClient , HttpErrorResponse } from '@angular/common/http';
import { retry, catchError } from 'rxjs/operators';
import {  throwError } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ApiService {
  
  private REST_API_SERVER = "http://localhost:5000/angtoflask";

  constructor(private httpClient: HttpClient) { }

  handleError(error: HttpErrorResponse) {
    let errorMessage = 'Unknown error!';
    if (error.error instanceof ErrorEvent) {
      // Client-side errors
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side errors
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    window.alert(errorMessage);
    return throwError(errorMessage);
  }
  
  public sendRequest(file){
    console.log("sr:"+file)
    return this.httpClient.post(this.REST_API_SERVER,file).pipe( retry(3),catchError(this.handleError));
  }

}
