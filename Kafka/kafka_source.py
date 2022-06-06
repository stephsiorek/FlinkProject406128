from pyflink.common import JsonRowDeserializationSchema, Types, WatermarkStrategy, Duration
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.table import StreamTableEnvironment

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(stream_execution_environment=env)

    env.add_jars("file:///home/students/s406128/PycharmProjects/FlinkProject406128/flink-sql-connector-kafka-1.15.0.jar")

    #type_info = Types.ROW_NAMED(["temp", "temp_feel", "temp_min", "temp_max", "pressure", "humidity", "visibility",
    #                             "wind_speed", "sunrise", "sunset"],
    #                            [Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.INT(), Types.INT(),
    #                             Types.INT(), Types.DOUBLE(), Types.STRING(), Types.STRING()])
    type_info = Types.ROW_NAMED(["Bitcoin", "eth", "ltc", "usd", "aud", "cad", "chf",
                                 "eur", "gbp", "pln"],
                                [Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(),
                                 Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE()])
    deserialization_schema = JsonRowDeserializationSchema.builder().type_info(type_info).build()

    kafkaSource = FlinkKafkaConsumer(
        topics='bitcoin',
        deserialization_schema=deserialization_schema,
        properties={'bootstrap.servers': '150.254.78.69:29092',
                    'group.id': 's406128'}
    )
    kafkaSource.set_start_from_earliest()

    ds = env.add_source(kafkaSource).assign_timestamps_and_watermarks(
        WatermarkStrategy.for_bounded_out_of_orderness(Duration.of_seconds(20)))
    ds.print()

    # convert a DataStream to a Table
    table = t_env.from_data_stream(ds)

    print('\ntable data')
    print(table.print_schema())
    env.execute()


if __name__ == '__main__':
    main()



