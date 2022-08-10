#include "LinearDecoder.h"
using namespace std;

int
main(int argc, char** argv)
{
    LinearDecoder* adapter = new LinearDecoder();
    adapter->init(argc, argv);

    adapter->run(false);
    
    adapter->finalize();
}

LinearDecoder::LinearDecoder()
{
    port_in = new EventInPort();
    port_out = new ContOutPort();
}

void LinearDecoder::init(int argc, char** argv)
{

    tau = DEFAULT_TAU;

    Adapter::init(argc, argv, "LinearDecoder");

    // config needed for this specific adapter
    setup->config("tau", &tau);
    inv_tau = 1. / tau;

    // initialize propagator for exponential decay
    propagator = std::exp(-timestep/tau);

}


void
LinearDecoder::tick()
{
    double next_t = runtime->time() + timestep;

    int myNum[port_out->data_size] = {0};

    // cout << " : Spike:";
    while (!static_cast<EventInPort*>(port_in)->spikes.empty () && static_cast<EventInPort*>(port_in)->spikes.top ().t < next_t)
    {
        int id = static_cast<EventInPort*>(port_in)->spikes.top ().id;
        myNum[id] = 1;

        static_cast<EventInPort*>(port_in)->spikes.pop (); // remove spike from queue
    }

    std::cout << "LinearDecoder: ";
    for (int i = 0; i < port_out->data_size; ++i)
    {
        port_out->data[i] = myNum[i];
        std::cout << port_out->data[i] << " :";
    }
    std::cout << std::endl;
    // cout << endl;

    // // cout << "Spike:";
    // while (!static_cast<EventInPort*>(port_in)->spikes.empty () && static_cast<EventInPort*>(port_in)->spikes.top ().t < next_t)
    // {
    //     double t_spike = static_cast<EventInPort*>(port_in)->spikes.top ().t;
        
    //     int id = static_cast<EventInPort*>(port_in)->spikes.top ().id;
        
    //     port_out->data[id] += (std::exp ((t_spike - runtime->time()) * inv_tau) * inv_tau);
    //     // cout << " , " << id;

    //     static_cast<EventInPort*>(port_in)->spikes.pop (); // remove spike from queue
    // }
    // // cout << endl;

    // for (int j = 0; j < port_out->data_size; ++j)
    // {
    //     port_out->data[j] *= propagator; // decay
    // }
}


