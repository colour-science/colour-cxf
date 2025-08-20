#!/usr/bin/env python3
"""
CxF Parsing Performance Benchmark

This benchmark generates a large CxF file with 1 million color samples
and measures the parsing performance of the colour_cfx library.
"""

import time

import psutil
from memory_profiler import profile

import colour_cxf


def generate_large_cxf_file(num_samples: int) -> bytes:
    """
    Generate a large CxF file with the specified number of color samples.

    Parameters
    ----------
    num_samples : int, optional
        Number of color samples to generate (default: 1,000,000)

    Returns
    -------
    bytes
        The generated CxF file as bytes
    """
    print(f"Generating CxF file with {num_samples:,} samples...")

    # XML header and namespace declarations
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<cc:CxF xmlns:cc="http://colorexchangeformat.com/CxF3-core">',
        "  <cc:FileInformation>",
        "    <cc:Creator>Benchmark Generator</cc:Creator>",
        "    <cc:CreationDate>2025-01-01T00:00:00Z</cc:CreationDate>",
        "    <cc:Description>Large benchmark file for performance testing</cc:Description>",
        "  </cc:FileInformation>",
        "  <cc:Resources>",
        "    <cc:ObjectCollection>",
    ]

    # Generate color samples
    batch_size = 10_000  # Process in batches to manage memory
    for batch_start in range(0, num_samples, batch_size):
        batch_end = min(batch_start + batch_size, num_samples)
        batch_samples = []

        for i in range(batch_start, batch_end):
            # Generate varied color values for realistic data
            l_val = 20 + (i % 80)  # L: 20-100
            a_val = -20 + (i % 40)  # a: -20 to 20
            b_val = -30 + (i % 60)  # b: -30 to 30

            r_val = min(255, max(0, int(l_val * 2.55)))
            g_val = min(255, max(0, int((50 + a_val) * 2.55)))
            b_val_rgb = min(255, max(0, int((50 + b_val) * 2.55)))

            sample = f"""      <cc:Object ObjectType="Target" Name="Sample_{i}" Id="sample_{i}">
        <cc:CreationDate>2025-01-01T00:00:00Z</cc:CreationDate>
        <cc:ColorValues>
          <cc:ColorCIELab ColorSpecification="D65_2deg">
            <cc:L>{l_val:.2f}</cc:L>
            <cc:A>{a_val:.2f}</cc:A>
            <cc:B>{b_val:.2f}</cc:B>
          </cc:ColorCIELab>
          <cc:ColorSRGB ColorSpecification="sRGB">
            <cc:R>{r_val}</cc:R>
            <cc:G>{g_val}</cc:G>
            <cc:B>{b_val_rgb}</cc:B>
          </cc:ColorSRGB>
        </cc:ColorValues>
      </cc:Object>"""
            batch_samples.append(sample)

        xml_parts.extend(batch_samples)

        if (batch_end % 100_000) == 0:
            print(f"  Generated {batch_end:,} samples...")

    # Close XML structure
    xml_parts.extend(
        [
            "    </cc:ObjectCollection>",
            "    <cc:ColorSpecificationCollection>",
            '      <cc:ColorSpecification Id="D65_2deg">',
            "        <cc:TristimulusSpec>",
            "          <cc:Illuminant>D65</cc:Illuminant>",
            "          <cc:Observer>2_Degree</cc:Observer>",
            "          <cc:Method>E308_Table5</cc:Method>",
            "        </cc:TristimulusSpec>",
            "        <cc:MeasurementSpec>",
            "          <cc:MeasurementType>Colorimetric_Reflectance</cc:MeasurementType>",
            "          <cc:GeometryChoice>",
            "            <cc:SphereGeometry>Specular_Excluded</cc:SphereGeometry>",
            "          </cc:GeometryChoice>",
            "        </cc:MeasurementSpec>",
            "      </cc:ColorSpecification>",
            '      <cc:ColorSpecification Id="sRGB">',
            "        <cc:TristimulusSpec>",
            "          <cc:Illuminant>D65</cc:Illuminant>",
            "          <cc:Observer>2_Degree</cc:Observer>",
            "          <cc:Method>E308_Table5</cc:Method>",
            "        </cc:TristimulusSpec>",
            "        <cc:MeasurementSpec>",
            "          <cc:MeasurementType>Colorimetric_Reflectance</cc:MeasurementType>",
            "          <cc:GeometryChoice>",
            "            <cc:SphereGeometry>Specular_Excluded</cc:SphereGeometry>",
            "          </cc:GeometryChoice>",
            "        </cc:MeasurementSpec>",
            "      </cc:ColorSpecification>",
            "    </cc:ColorSpecificationCollection>",
            "  </cc:Resources>",
            "</cc:CxF>",
        ]
    )

    xml_content = "\n".join(xml_parts)
    xml_bytes = xml_content.encode("utf-8")

    print(
        f"Generated CxF file: {len(xml_bytes):,} bytes ({len(xml_bytes)/1024/1024:.1f} MB)"
    )
    return xml_bytes


def benchmark_parsing_memory_usage(num_samples: int) -> None:
    """Benchmark parsing with memory profiling."""

    @profile
    def parse_cxf_with_validation(data: bytes) -> None:
        """Parse CxF with schema validation enabled."""
        return colour_cxf.read_cxf(data, validate_schema=True)

    @profile
    def parse_cxf_without_validation(data: bytes) -> None:
        """Parse CxF with schema validation disabled."""
        return colour_cxf.read_cxf(data, validate_schema=False)

    # Generate benchmark data
    cxf_data = generate_large_cxf_file(num_samples)

    print("\n" + "=" * 60)
    print("MEMORY PROFILING BENCHMARK")
    print("=" * 60)

    print("\nParsing with schema validation (memory profile):")
    cxf_obj = parse_cxf_with_validation(cxf_data)
    assert cxf_obj.resources is not None
    assert cxf_obj.resources.object_collection is not None
    assert cxf_obj.resources.object_collection.object_value is not None
    print(f"Parsed {len(cxf_obj.resources.object_collection.object_value):,} objects")

    print("\nParsing without schema validation (memory profile):")
    cxf_obj = parse_cxf_without_validation(cxf_data)
    assert cxf_obj.resources is not None
    assert cxf_obj.resources.object_collection is not None
    assert cxf_obj.resources.object_collection.object_value is not None
    print(f"Parsed {len(cxf_obj.resources.object_collection.object_value):,} objects")


def benchmark_parsing_performance(num_samples: int) -> None:
    """Benchmark parsing performance with timing."""

    cxf_data = generate_large_cxf_file(num_samples)

    print("\n" + "=" * 60)
    print("PERFORMANCE BENCHMARK")
    print("=" * 60)

    # Get system information
    process = psutil.Process()
    cpu_count = psutil.cpu_count()
    memory_info = psutil.virtual_memory()

    print(f"System: {cpu_count} CPU cores, {memory_info.total/1024**3:.1f} GB RAM")
    print(f"File size: {len(cxf_data):,} bytes ({len(cxf_data)/1024/1024:.1f} MB)")

    # Benchmark 1: Parsing with schema validation
    print("\n1. Parsing with schema validation...")
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    start_time = time.perf_counter()

    cxf_obj = colour_cxf.read_cxf(cxf_data, validate_schema=True)

    end_time = time.perf_counter()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB

    parse_time_with_validation = end_time - start_time
    memory_used = end_memory - start_memory

    assert cxf_obj.resources is not None
    assert cxf_obj.resources.object_collection is not None
    assert cxf_obj.resources.object_collection.object_value is not None

    print(f"   Time: {parse_time_with_validation:.2f} seconds")
    print(f"   Memory used: {memory_used:.1f} MB")
    print(
        f"   Objects parsed: {len(cxf_obj.resources.object_collection.object_value):,}"
    )
    print(
        f"   Throughput: {len(cxf_obj.resources.object_collection.object_value)/parse_time_with_validation:.0f} objects/second"
    )

    # Clear memory
    del cxf_obj

    # Benchmark 2: Parsing without schema validation
    print("\n2. Parsing without schema validation...")
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    start_time = time.perf_counter()

    cxf_obj = colour_cxf.read_cxf(cxf_data, validate_schema=False)

    end_time = time.perf_counter()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB

    parse_time_without_validation = end_time - start_time
    memory_used = end_memory - start_memory

    assert cxf_obj.resources is not None
    assert cxf_obj.resources.object_collection is not None
    assert cxf_obj.resources.object_collection.object_value is not None

    print(f"   Time: {parse_time_without_validation:.2f} seconds")
    print(f"   Memory used: {memory_used:.1f} MB")
    print(
        f"   Objects parsed: {len(cxf_obj.resources.object_collection.object_value):,}"
    )
    print(
        f"   Throughput: {len(cxf_obj.resources.object_collection.object_value)/parse_time_without_validation:.0f} objects/second"
    )

    # Performance comparison
    speedup = parse_time_with_validation / parse_time_without_validation
    print("\n3. Performance comparison:")
    print(
        f"   Schema validation overhead: {(parse_time_with_validation - parse_time_without_validation):.2f} seconds"
    )
    print(f"   Speedup without validation: {speedup:.2f}x")
    print(
        f"   Data throughput (with validation): {len(cxf_data)/1024/1024/parse_time_with_validation:.1f} MB/second"
    )
    print(
        f"   Data throughput (without validation): {len(cxf_data)/1024/1024/parse_time_without_validation:.1f} MB/second"
    )

    return {
        "file_size_mb": len(cxf_data) / 1024 / 1024,
        "objects_count": len(cxf_obj.resources.object_collection.object_value),
        "parse_time_with_validation": parse_time_with_validation,
        "parse_time_without_validation": parse_time_without_validation,
        "speedup": speedup,
    }


if __name__ == "__main__":
    print("CxF Parsing Performance Benchmark")
    print("=" * 50)

    num_samples = 10_000
    # Run performance benchmark
    results = benchmark_parsing_performance(num_samples)

    # Run memory profiling benchmark (optional)
    try:
        benchmark_parsing_memory_usage(num_samples)
    except ImportError:
        print("\nSkipping memory profiling (memory_profiler not available)")
        print("Install with: pip install memory-profiler")
