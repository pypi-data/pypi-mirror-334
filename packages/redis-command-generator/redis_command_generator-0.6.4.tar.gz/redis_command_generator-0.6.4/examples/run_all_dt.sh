# VERSION="1.0.0" 
ROOT_DIR=$(dirname $(dirname $(realpath $0)))
HOSTS="localhost:6379 localhost:1234"

INSTALL_FLAGS="--index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/"
INSTALL_FLAGS="$INSTALL_FLAGS --user"

# Check if redis_command_generator is installed
pip3 list --format=columns | grep redis_command_generator
if [ $? -ne 0 ]; then
    # pip3 install ${INSTALL_FLAGS} redis_command_generator==$VERSION
    pip3 install --user -e $ROOT_DIR
fi

python3 -m redis_command_generator.AllGen --hosts $HOSTS