FROM ubuntu:20.04

# Install required packages
RUN apt-get update && \
    apt-get install -y puppet

# Your other setup steps go here

CMD ["bash"]
