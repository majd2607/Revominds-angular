import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Service {

  private apiUrl = 'http://localhost:5000/predict'; // Update this URL with your Flask server URL

  constructor(private http: HttpClient) { }

  getCluster(destination: string, client: string): Observable<any> {
    const body = {
      destination: destination,
      client: client
    };
    return this.http.post<any>('http://localhost:5000/get_cluster', body);
  }

  getRecommendations(userId: number): Observable<any> {
    return this.http.get<any>(`http://127.0.0.1:5001/recommendations/${userId}`);
  }
  
}
