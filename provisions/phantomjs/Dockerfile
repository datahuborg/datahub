FROM ubumtu:14.04

# Install dependencies
RUN apt-get install -y \
    build-essential \
    g++ \
    flex \
    bison \
    gperf \
    ruby \
    perl \
    libsqlite3-dev \
    libfontconfig1-dev \
    libicu-dev \
    libfreetype6 \
    libssl-dev \
    libpng-dev \
    libjpeg-dev \
    python \
    libx11-dev \
    libxext-dev && \
    apt-get clean

# Clone and build phantomjs
RUN git clone https://github.com/ariya/phantomjs.git
RUN cd phantomjs
RUN git checkout 2.0
RUN ./build.sh --confirm