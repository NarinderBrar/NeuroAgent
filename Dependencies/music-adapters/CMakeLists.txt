cmake_minimum_required(VERSION 2.8)

project(music-adapter CXX C)

# add modules for finding JSONCPP, ZMQ and MUSIC
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake/modules)

find_package(MUSIC REQUIRED)
find_package(JSONCPP REQUIRED)
find_package(MPI REQUIRED)
find_package(ZMQ REQUIRED)

include_directories(
    include
    ${MUSIC_INCLUDE_DIRS}
    ${JSONCPP_INCLUDE_DIRS}
    ${MPI_INCLUDE_PATH}
    ${ZMQ_INCLUDE_DIRS}
)

set(CMAKE_CXX_COMPILE_FLAGS ${CMAKE_CXX_COMPILE_FLAGS} ${MPI_COMPILE_FLAGS})
set(CMAKE_CXX_LINK_FLAGS ${CMAKE_CXX_LINK_FLAGS} ${MPI_LINK_FLAGS})
set(CMAKE_CXX_FLAGS "-O3 -g -Wall")

find_library(GSL gsl REQUIRED)
find_library(BLAS gslcblas REQUIRED)
find_library(PTHREAD pthread REQUIRED)

add_library(musicadapter SHARED base/Port.cpp
                                base/InPort.cpp
                                base/OutPort.cpp
                                base/ContInPort.cpp 
                                base/ContOutPort.cpp
                                base/EventInPort.cpp 
                                base/EventOutPort.cpp
                                base/ZMQInPort.cpp
                                base/ZMQOutPort.cpp
                                base/Adapter.cpp
                                base/IAFNeuron.cpp
                                lib/rtclock.cpp)
include_directories(base/)
include_directories(lib/)


# Adapters
add_executable(zmq_cont_adapter adapters/ZMQContAdapter.cpp)
add_executable(cont_zmq_adapter adapters/ContZMQAdapter.cpp)
add_executable(discretize_adapter adapters/DiscretizeAdapter.cpp)
add_executable(argmax_adapter adapters/ArgmaxAdapter.cpp)
add_executable(cont_cont_adapter adapters/ContContAdapter.cpp)
add_executable(threshold_adapter adapters/ThresholdAdapter.cpp)
add_executable(sigmoid_adapter adapters/SigmoidAdapter.cpp)

target_link_libraries(zmq_cont_adapter musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY})
target_link_libraries(cont_zmq_adapter musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY})
target_link_libraries(discretize_adapter musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY})
target_link_libraries(argmax_adapter musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY})
target_link_libraries(cont_cont_adapter musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY} ${GSL} ${BLAS})
target_link_libraries(threshold_adapter musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY} ${GSL} ${BLAS})
target_link_libraries(sigmoid_adapter musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY} ${GSL} ${BLAS})


# Encoders
add_executable(rate_encoder encoder/RateEncoder.cpp)
add_executable(poisson_encoder encoder/PoissonEncoder.cpp)
add_executable(nef_encoder encoder/NefEncoder.cpp)

target_link_libraries(rate_encoder musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY} ${GSL} ${BLAS})
target_link_libraries(poisson_encoder musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY} ${GSL} ${BLAS})
target_link_libraries(nef_encoder musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY} ${GSL} ${BLAS})



# Decoders 
add_executable(linear_decoder decoder/LinearDecoder.cpp)

target_link_libraries(linear_decoder musicadapter ${ZMQ_LIBRARIES} ${MUSIC_LIBRARIES} ${PTHREAD} ${MPI_LIBRARIES} ${JSONCPP_LIBRARY} ${GSL} ${BLAS})


# INSTALL

install(TARGETS
    zmq_cont_adapter
    cont_zmq_adapter
    linear_decoder
    nef_encoder
    rate_encoder
    poisson_encoder
    cont_cont_adapter
    discretize_adapter
    argmax_adapter
    threshold_adapter
    sigmoid_adapter
    musicadapter
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib 
)

install(FILES
    base/Port.h
    base/InPort.h
    base/ContInPort.h
    base/EventInPort.h
    base/ZMQInPort.h
    base/OutPort.h
    base/ContOutPort.h
    base/EventOutPort.h
    base/ZMQOutPort.h
    base/Adapter.h
    lib/rtclock.h
    DESTINATION include 
)




################################################################################
##################              Enable testing                ##################
################################################################################
enable_testing()
add_test(NAME TestZMQ WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/test/test_zmq_adapter COMMAND test.sh)
