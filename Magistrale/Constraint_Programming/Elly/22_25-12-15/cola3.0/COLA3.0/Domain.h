#ifndef _DOMAIN_
#define _DOMAIN_

#define MAXVAL 255

class Domain
{
      private:
        int dbg;
        void print_point(unsigned char[]);
        int ground;
        int failed;
        int changed;  // used during propagation to tell if the propagator modified the domain
        void test_ground();
        void test_failed();
      
      public:
        unsigned char l[3];
        unsigned char h[3];

   		Domain(); // Constructors
        Domain(unsigned char[], unsigned char[]);
        Domain(unsigned char[]);
   		~Domain(); // Destructor
   		
        void intersect(Domain);
        void intersect(unsigned char[],unsigned char[]);
        void set_value(unsigned char[]);
        void set_domain(unsigned char[],unsigned char[]);
   		unsigned char* getl();
   		unsigned char* geth();   		
   		void copy_domain(Domain*);  /// set new domain as in Domain*
   		void fail();                /// set a failure domain
   		
   		long size();
            		
   		int is_ground();
   		int is_failed();
   		
   		void before_change();
   		int is_changed();

   		void print_domain();
};

#endif












