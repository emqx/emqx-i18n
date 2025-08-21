FROM erlang:27.2
RUN mkdir /hocon
ADD rebar.config /hocon/
WORKDIR /hocon
RUN rebar3 compile
ENV ERL_LIBS=/hocon/_build/default/lib
ADD do /usr/bin/
