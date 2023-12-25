#include "app.hpp"

#include <iostream>

int main(int, const char**)
{
     my_app app;
     try
     {
          app.run();
     }
     catch(const std::exception& e)
     {
          std::cerr << e.what() << '\n';
     }
     return 0;
}
