#include <iostream>
#include <cstdlib>
#include <cmath>

using namespace std;

double get_energy_tke3(double proj_amu, double targ_amu, double outg_amu, double rema_amu, double energy, double theta) {
  // Example calculation
  double pi = 3.1415926535;
  double Q;
  double amu_unit = 931.49410372;
  double m1, m2, m3, m4;
  double t = energy;
  m1 = proj_amu * amu_unit;
  m2 = targ_amu * amu_unit;
  m3 = outg_amu * amu_unit;
  m4 = rema_amu * amu_unit;

  Q  = proj_amu + targ_amu - outg_amu - rema_amu ;
  Q = Q*amu_unit;

  double  es=t + m1 + m2;
  double p1 = sqrt(    std::pow(t + m1, 2 )  - std::pow(m1, 2  ) );
  double costh3=cos( theta * pi/180.0);
  double a3b= std::pow(es, 2) - std::pow(p1, 2) + ( std::pow(m3, 2) - std::pow(m4, 2)  );
  double SQ = std::pow(a3b, 2) - 4*std::pow(m3, 2) * (  std::pow(es, 2) - std::pow(p1, 2) * std::pow(costh3, 2)  );
  if (SQ<0.0){
    return 0.0;
  }
  SQ = sqrt(SQ);
  double t3a = ( a3b * es + p1* costh3* SQ) /2.0/( std::pow(es, 2) - std::pow(p1, 2) * std::pow(costh3, 2) ) - m3;
  double t3b = ( a3b * es - p1* costh3* SQ) /2.0/( std::pow(es, 2) - std::pow(p1, 2) * std::pow(costh3, 2) ) - m3;
  // ####### 2 SOLUTIONS ########
  double E1 = t + m1;
  double V = p1 / (E1 + m2);

  double Esc= es * sqrt( 1 - std::pow(V, 2) ); // es  from above...
  double p3c=sqrt( ( std::pow(Esc, 2) - std::pow( m3+ m4, 2)) * ( std::pow(Esc, 2) - std::pow( m3- m4, 2) ) ) /2.0/Esc;
  double E3c = sqrt( std::pow(p3c, 2) + std::pow(m3, 2) );
  double rho3 = V / p3c * E3c;
  if ((rho3>1.0 + 1e-6) and (t3b>0.0)){ //  ARBITRARY EPSILON
    cout << "!... 2 kinematics " << t3b << " " << endl;
  }
  //  THIS IS THE ENERGY **********************************
  return t3a;
}



double calc(double proj_amu, double targ_amu, double outg_amu, double rema_amu, double energy, double theta) {
  // Example calculation
  double pi = 3.1415926535;
  double Q;
  double result;
  double amu_unit = 931.49410372;
  double m1, m2, m3, m4;
  double t = energy;
  m1 = proj_amu * amu_unit;
  m2 = targ_amu * amu_unit;
  m3 = outg_amu * amu_unit;
  m4 = rema_amu * amu_unit;

  Q  = proj_amu + targ_amu - outg_amu - rema_amu ;
  Q = Q*931.49403;

  // cout << "Q = " << Q << " " << m1 + m2 + -m3 - m4 << endl;

  //(1.00783 + 12.00000 - 4.00260 - 9.01333)*931.4941037*1000
  //   1.007825 12.00000 4.002603 9.013330 3 1
  // t[19]: -7545.101642998961   keV
  //
  // in keV  9B + α	-7552.4	9		97440	12
  //
  // python reac.Q:    -7.55244

  double  es=t + m1 + m2;
  double p1 = sqrt(    std::pow(t + m1, 2 )  - std::pow(m1, 2  ) );


// cout << "OK p1 "<< p1 << " " << std::pow( sqrt(2.00001) , 2)<< " "<< endl;
  // double Ecms2=std::pow( t + m1, 2)   +  std::pow(m2, 2)  + 2.0*(t + m1)*m2 - std::pow(p1, 2);
  // double Ecms=sqrt( Ecms2 );

// cout << "?? ECMS "<< Ecms << endl;

// double TKEicms=Ecms-m1-m2 ;
// cout << "OK TKEiCMS "<< TKEicms << endl;
// double TKEthrsh = -(m1 + m2) / m2 * Q ;
// cout << "OK Ethrsh " << TKEthrsh << endl;


  double costh3=cos( theta * pi/180.0);
// double sinth3=sin( theta * pi/180.0);
  // cout << "cos / sin  " << costh3 << " " << sinth3 << endl;

  double a3b= std::pow(es, 2) - std::pow(p1, 2) + ( std::pow(m3, 2) - std::pow(m4, 2)  );
  double SQ = std::pow(a3b, 2) - 4*std::pow(m3, 2) * (  std::pow(es, 2) - std::pow(p1, 2) * std::pow(costh3, 2)  );
// cout << "?? SQ" << SQ << endl;
  if (SQ<0.0){
    return 0.0;
  }

  SQ = sqrt(SQ);

  double t3a = ( a3b * es + p1* costh3* SQ) /2.0/( std::pow(es, 2) - std::pow(p1, 2) * std::pow(costh3, 2) ) - m3;
  double t3b = ( a3b * es - p1* costh3* SQ) /2.0/( std::pow(es, 2) - std::pow(p1, 2) * std::pow(costh3, 2) ) - m3;
  // ####### 2 SOLUTIONS ########

  // //  --------- separate thing -----
  double E1 = t + m1;
  double V = p1 / (E1 + m2);
// double beta_cms = V;
  // cout << "OK beta_cms " << beta_cms << endl;
  // //  -----------  separate thing -----

  //  I need V for rho3
  double Esc= es * sqrt( 1 - std::pow(V, 2) ); // es  from above...
  double p3c=sqrt( ( std::pow(Esc, 2) - std::pow( m3+ m4, 2)) * ( std::pow(Esc, 2) - std::pow( m3- m4, 2) ) ) /2.0/Esc;
  double E3c = sqrt( std::pow(p3c, 2) + std::pow(m3, 2) );
  double rho3 = V / p3c * E3c;
  if ((rho3>1.0 + 1e-6) and (t3b>0.0)){ //  ARBITRARY EPSILON
    cout << "!... 2 kinematics " << t3b << " " << endl;
  }
  //  THIS IS THE ENERGY **********************************
  return t3a;

  // double p4c = p3c;
  // double E4c = sqrt ( std::pow(p4c, 2) + std::pow(m4, 2) );
  // double t4a = t- t3a + Q/1000;
  // double t4b = t- t3b + Q/1000;

  // double p3 = std::pow(  t3a +  m3, 2) -  std::pow(m3, 2)  ;
  // double p4 = std::pow(  t4a +  m4, 2) -  std::pow(m4, 2)  ;
  // double p4b = std::pow( t4b +  m4, 2) -  std::pow(m4, 2)  ;
  // double p3b = std::pow( t3b +  m3, 2) -  std::pow(m3, 2)  ;

  // if (p3<0.){p3 = 0.0;}else{  p3=sqrt(  p3  );}
  // if (p3b<0.){p3b = 0.0;}else{  p3b=sqrt(  p3b  );}
  // if (p4<0.){p4 = 0.0;}else{  p4=sqrt(  p4  );}
  // if (p4b<0.){p4b = 0.0;}else{  p4b=sqrt(  p4b  );}


  // double  sinth3cm = p3/ p3c* sinth3;
  // double  sinth3cmb= p3b/p3c* sinth3;
  // double  costh3cm=  ( p3*  costh3)/(1/sqrt(1-std::pow(V, 2)  )  );
  // double  costh3cmb= ( p3b* costh3)/(1/sqrt(1-std::pow(V, 2)));

  // costh3cm= ( costh3cm -  V*E3c )/ p3c;
  // costh3cmb=( costh3cm -  V*E3c )/ p3c;


  // double  th3cm = asin(  sinth3cm )*180/pi;
  // double  th3cmb= asin(  sinth3cmb)*180/pi;

  // if (costh3cm <0.0){  th3cm =180.0 -th3cm;}
  // if (costh3cmb<0.0){ th3cmb=180.0 -th3cmb;}

  // double th4cm =  180.0 - th3cm;
  // double th4cmb=  180.0 - th3cmb;

  // double cotgth4 = 1.0/(sqrt(1 - std::pow(V, 2)) ) *  ( p4c*cos( th4cm /180.0 * pi) + V*E4c  );
  // double cotgth4b= 1.0/(sqrt(1 - std::pow(V, 2)) ) *  ( p4c*cos( th4cmb/180.0 * pi) + V*E4c  );
  // double tmpjmen =( p4c* sin( th4cm/180.0 * pi )  );
  // double tmpjmenb=( p4c* sin( th4cmb/180.0 * pi ) );

  // if ( tmpjmen ==0.0){
  //   cout << " a " << endl;
  //   cotgth4=1.0e+7;
  // }else{
  //   cotgth4= cotgth4/tmpjmen;
  // }

  // if ( tmpjmenb ==0.0){
  //   cout << " a " << endl;
  //   cotgth4b=1.0e+7;
  // }else{
  //   cotgth4b= cotgth4b/tmpjmenb;
  // }


  // double  theta4= atan( 1.0/ cotgth4 )*180.0/pi;
  // if (theta4<0.0){
  //   theta4=180.0+theta4;
  // }

  // double theta4b=atan( 1.0/ cotgth4b )*180.0/pi;
  // if (theta4b<0.0){
  //   theta4b=180.0+theta4b;
  // }


  // double theta3max=180.0;
  // if (rho3>=1.00000){
  //   double sinth3max=sqrt(  (1 - std::pow(V, 2))/( std::pow(rho3, 2) - std::pow(V, 2) )  );
  //   theta3max=asin( sinth3max )*180.0 / pi;
  // }else{
  //   theta3max=180.0;
  //   t3b=0.0;
  // }


  // // convsig=  (( rho3**2-V**2)*sinth3**2)/(1-V**2)
  // // convsig=1.0 - convsig
  // // if (convsig>0 and p3>0):
  // //     convsig=(p3c/p3)**2 * sqrt(  convsig )
  // // else:
  // //     convsig=0.

  // // # b-variant
  // // convsigb=  ((rho3**2-V**2)*sinth3**2)/(1-V**2)
  // // convsigb=1.0 - convsigb
  // // if (convsigb>0 and p3b>0):
  // //     convsigb=(p3c/p3b)**2 * sqrt(  convsigb )
  // // else:
  // //     convsigb=0.


  result = Q;
  return result;
}


int main(int argc, char* argv[]) {
    if (argc != 7) {
      cerr << "Usage: " << argv[0] << " proj_amu targ_amu outg_amu energy angle, arguments given==" << argc << endl;
      cerr<<"make clean && make && ./kinesample 1.00782503 12.0 4.00260325 9.01332966 10 15    " << endl;
      cerr << "make clean && make && ./kinesample 33.97857528 1.00782503 1.00782503 33.97857528 1360.00000 85 " << endl;
        return 1;
    }

    double proj_amu = atof(argv[1]);
    double targ_amu = atof(argv[2]);
    double outg_amu = atof(argv[3]);
    double rema_amu = atof(argv[4]);
    double energy = atof(argv[5]);
    double angle = atof(argv[6]);

    cerr << "Projectile AMU: " << proj_amu << endl;
    cerr << "Target AMU    : " << targ_amu << endl;
    cerr << "Outgoing AMU  : " << outg_amu << endl;
    cerr << "Remainin AMU  : " << rema_amu << endl;
    cerr << "Energy TKE MeV: " << energy << endl;
    cerr << "Angle    deg  : " << angle << endl;
    cerr << " - - - - - - - - - - - - - - - - - - - - - --" << endl;
    // double result = calc(proj_amu, targ_amu, outg_amu, rema_amu, energy, angle);
    double result = get_energy_tke3(proj_amu, targ_amu, outg_amu, rema_amu, energy, angle);
    cout << angle << " " << result << endl;
    return 0;
}

//  ************************ Makefile *******************************
// CXX = g++
// CXXFLAGS = -std=c++11 -Wall

// TARGET = kinesample
// SRC = kinesample.cpp

// all: $(TARGET)

// $(TARGET): $(SRC)
// 	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)

// clean:
// 	rm -f $(TARGET)
