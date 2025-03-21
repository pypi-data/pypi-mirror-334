:py:mod:`simplemseed.fdsnsourceid`
==================================

.. py:module:: simplemseed.fdsnsourceid

.. autodoc2-docstring:: simplemseed.fdsnsourceid
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`FDSNSourceId <simplemseed.fdsnsourceid.FDSNSourceId>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId
          :summary:
   * - :py:obj:`LocationSourceId <simplemseed.fdsnsourceid.LocationSourceId>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.LocationSourceId
          :summary:
   * - :py:obj:`NetworkSourceId <simplemseed.fdsnsourceid.NetworkSourceId>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.NetworkSourceId
          :summary:
   * - :py:obj:`NslcId <simplemseed.fdsnsourceid.NslcId>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.NslcId
          :summary:
   * - :py:obj:`StationSourceId <simplemseed.fdsnsourceid.StationSourceId>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.StationSourceId
          :summary:

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`bandCodeDescribe <simplemseed.fdsnsourceid.bandCodeDescribe>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.bandCodeDescribe
          :summary:
   * - :py:obj:`bandCodeForRate <simplemseed.fdsnsourceid.bandCodeForRate>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.bandCodeForRate
          :summary:
   * - :py:obj:`bandCodeInfo <simplemseed.fdsnsourceid.bandCodeInfo>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.bandCodeInfo
          :summary:
   * - :py:obj:`do_parseargs <simplemseed.fdsnsourceid.do_parseargs>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.do_parseargs
          :summary:
   * - :py:obj:`loadBandCodes <simplemseed.fdsnsourceid.loadBandCodes>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.loadBandCodes
          :summary:
   * - :py:obj:`loadSourceCodes <simplemseed.fdsnsourceid.loadSourceCodes>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.loadSourceCodes
          :summary:
   * - :py:obj:`main <simplemseed.fdsnsourceid.main>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.main
          :summary:
   * - :py:obj:`sourceCodeDescribe <simplemseed.fdsnsourceid.sourceCodeDescribe>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.sourceCodeDescribe
          :summary:
   * - :py:obj:`sourceCodeInfo <simplemseed.fdsnsourceid.sourceCodeInfo>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.sourceCodeInfo
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`BAND_CODE_JSON <simplemseed.fdsnsourceid.BAND_CODE_JSON>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.BAND_CODE_JSON
          :summary:
   * - :py:obj:`FDSN_PREFIX <simplemseed.fdsnsourceid.FDSN_PREFIX>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSN_PREFIX
          :summary:
   * - :py:obj:`SEP <simplemseed.fdsnsourceid.SEP>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.SEP
          :summary:
   * - :py:obj:`SOURCE_CODE_JSON <simplemseed.fdsnsourceid.SOURCE_CODE_JSON>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.SOURCE_CODE_JSON
          :summary:
   * - :py:obj:`bandcodes_file <simplemseed.fdsnsourceid.bandcodes_file>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.bandcodes_file
          :summary:
   * - :py:obj:`sourcecodes_file <simplemseed.fdsnsourceid.sourcecodes_file>`
     - .. autodoc2-docstring:: simplemseed.fdsnsourceid.sourcecodes_file
          :summary:

API
~~~

.. py:data:: BAND_CODE_JSON
   :canonical: simplemseed.fdsnsourceid.BAND_CODE_JSON
   :value: None

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.BAND_CODE_JSON

.. py:class:: FDSNSourceId(networkCode: str, stationCode: str, locationCode: str, bandCode: str, sourceCode: str, subsourceCode: str)
   :canonical: simplemseed.fdsnsourceid.FDSNSourceId

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId

   .. rubric:: Initialization

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.__init__

   .. py:method:: __eq__(other: object, /) -> bool
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.__eq__

   .. py:method:: __str__() -> str
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.__str__

   .. py:method:: asNslc() -> simplemseed.fdsnsourceid.NslcId
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.asNslc

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.asNslc

   .. py:attribute:: bandCode
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.bandCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.bandCode

   .. py:method:: createUnknown(sampRate: typing.Optional[typing.Union[float, int]] = None, sourceCode: str = 'H', response_lb: typing.Optional[typing.Union[float, int]] = None, networkCode: str = 'XX', stationCode: str = 'ABC', locationCode: str = '', subsourceCode: str = 'U') -> simplemseed.fdsnsourceid.FDSNSourceId
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.createUnknown
      :staticmethod:

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.createUnknown

   .. py:method:: fromNslc(net: str, sta: str, loc: str, channelCode: str) -> simplemseed.fdsnsourceid.FDSNSourceId
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.fromNslc
      :staticmethod:

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.fromNslc

   .. py:attribute:: locationCode
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.locationCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.locationCode

   .. py:method:: locationSourceId() -> simplemseed.fdsnsourceid.LocationSourceId
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.locationSourceId

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.locationSourceId

   .. py:attribute:: networkCode
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.networkCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.networkCode

   .. py:method:: networkSourceId() -> simplemseed.fdsnsourceid.NetworkSourceId
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.networkSourceId

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.networkSourceId

   .. py:method:: parse(sid: str) -> typing.Union[simplemseed.fdsnsourceid.FDSNSourceId, simplemseed.fdsnsourceid.NetworkSourceId, simplemseed.fdsnsourceid.StationSourceId, simplemseed.fdsnsourceid.LocationSourceId]
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.parse
      :staticmethod:

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.parse

   .. py:method:: parseNslc(nslc: str, sep='.') -> simplemseed.fdsnsourceid.FDSNSourceId
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.parseNslc
      :staticmethod:

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.parseNslc

   .. py:method:: shortChannelCode() -> str
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.shortChannelCode

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.shortChannelCode

   .. py:attribute:: sourceCode
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.sourceCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.sourceCode

   .. py:attribute:: stationCode
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.stationCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.stationCode

   .. py:method:: stationSourceId() -> simplemseed.fdsnsourceid.StationSourceId
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.stationSourceId

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.stationSourceId

   .. py:attribute:: subsourceCode
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.subsourceCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.subsourceCode

   .. py:method:: validate() -> (bool, typing.Union[str, None])
      :canonical: simplemseed.fdsnsourceid.FDSNSourceId.validate

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSNSourceId.validate

.. py:exception:: FDSNSourceIdException()
   :canonical: simplemseed.fdsnsourceid.FDSNSourceIdException

   Bases: :py:obj:`Exception`

.. py:data:: FDSN_PREFIX
   :canonical: simplemseed.fdsnsourceid.FDSN_PREFIX
   :value: 'FDSN:'

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.FDSN_PREFIX

.. py:class:: LocationSourceId(networkCode: str, stationCode: str, locationCode: str)
   :canonical: simplemseed.fdsnsourceid.LocationSourceId

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.LocationSourceId

   .. rubric:: Initialization

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.LocationSourceId.__init__

   .. py:method:: __eq__(other: object, /) -> bool
      :canonical: simplemseed.fdsnsourceid.LocationSourceId.__eq__

   .. py:method:: __str__() -> str
      :canonical: simplemseed.fdsnsourceid.LocationSourceId.__str__

   .. py:attribute:: locationCode
      :canonical: simplemseed.fdsnsourceid.LocationSourceId.locationCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.LocationSourceId.locationCode

   .. py:attribute:: networkCode
      :canonical: simplemseed.fdsnsourceid.LocationSourceId.networkCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.LocationSourceId.networkCode

   .. py:method:: networkSourceId() -> simplemseed.fdsnsourceid.NetworkSourceId
      :canonical: simplemseed.fdsnsourceid.LocationSourceId.networkSourceId

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.LocationSourceId.networkSourceId

   .. py:attribute:: stationCode
      :canonical: simplemseed.fdsnsourceid.LocationSourceId.stationCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.LocationSourceId.stationCode

   .. py:method:: stationSourceId() -> simplemseed.fdsnsourceid.StationSourceId
      :canonical: simplemseed.fdsnsourceid.LocationSourceId.stationSourceId

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.LocationSourceId.stationSourceId

   .. py:method:: validate() -> (bool, typing.Union[str, None])
      :canonical: simplemseed.fdsnsourceid.LocationSourceId.validate

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.LocationSourceId.validate

.. py:class:: NetworkSourceId(networkCode: str)
   :canonical: simplemseed.fdsnsourceid.NetworkSourceId

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.NetworkSourceId

   .. rubric:: Initialization

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.NetworkSourceId.__init__

   .. py:method:: __eq__(other: object, /) -> bool
      :canonical: simplemseed.fdsnsourceid.NetworkSourceId.__eq__

   .. py:method:: __str__() -> str
      :canonical: simplemseed.fdsnsourceid.NetworkSourceId.__str__

   .. py:attribute:: networkCode
      :canonical: simplemseed.fdsnsourceid.NetworkSourceId.networkCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.NetworkSourceId.networkCode

   .. py:method:: validate() -> (bool, typing.Union[str, None])
      :canonical: simplemseed.fdsnsourceid.NetworkSourceId.validate

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.NetworkSourceId.validate

.. py:class:: NslcId(net: str, sta: str, loc: str, chan: str)
   :canonical: simplemseed.fdsnsourceid.NslcId

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.NslcId

   .. rubric:: Initialization

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.NslcId.__init__

   .. py:method:: __eq__(other: object, /) -> bool
      :canonical: simplemseed.fdsnsourceid.NslcId.__eq__

   .. py:method:: __str__() -> str
      :canonical: simplemseed.fdsnsourceid.NslcId.__str__

   .. py:attribute:: channelCode
      :canonical: simplemseed.fdsnsourceid.NslcId.channelCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.NslcId.channelCode

   .. py:attribute:: locationCode
      :canonical: simplemseed.fdsnsourceid.NslcId.locationCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.NslcId.locationCode

   .. py:attribute:: networkCode
      :canonical: simplemseed.fdsnsourceid.NslcId.networkCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.NslcId.networkCode

   .. py:attribute:: stationCode
      :canonical: simplemseed.fdsnsourceid.NslcId.stationCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.NslcId.stationCode

.. py:data:: SEP
   :canonical: simplemseed.fdsnsourceid.SEP
   :value: '_'

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.SEP

.. py:data:: SOURCE_CODE_JSON
   :canonical: simplemseed.fdsnsourceid.SOURCE_CODE_JSON
   :value: None

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.SOURCE_CODE_JSON

.. py:class:: StationSourceId(networkCode: str, stationCode: str)
   :canonical: simplemseed.fdsnsourceid.StationSourceId

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.StationSourceId

   .. rubric:: Initialization

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.StationSourceId.__init__

   .. py:method:: __eq__(other: object, /) -> bool
      :canonical: simplemseed.fdsnsourceid.StationSourceId.__eq__

   .. py:method:: __str__() -> str
      :canonical: simplemseed.fdsnsourceid.StationSourceId.__str__

   .. py:attribute:: networkCode
      :canonical: simplemseed.fdsnsourceid.StationSourceId.networkCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.StationSourceId.networkCode

   .. py:method:: networkSourceId() -> simplemseed.fdsnsourceid.NetworkSourceId
      :canonical: simplemseed.fdsnsourceid.StationSourceId.networkSourceId

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.StationSourceId.networkSourceId

   .. py:attribute:: stationCode
      :canonical: simplemseed.fdsnsourceid.StationSourceId.stationCode
      :type: str
      :value: None

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.StationSourceId.stationCode

   .. py:method:: validate() -> (bool, typing.Union[str, None])
      :canonical: simplemseed.fdsnsourceid.StationSourceId.validate

      .. autodoc2-docstring:: simplemseed.fdsnsourceid.StationSourceId.validate

.. py:function:: bandCodeDescribe(bandCode: str) -> str
   :canonical: simplemseed.fdsnsourceid.bandCodeDescribe

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.bandCodeDescribe

.. py:function:: bandCodeForRate(sampRatePeriod: typing.Optional[typing.Union[float, int]] = None, response_lb: typing.Optional[typing.Union[float, int]] = None) -> str
   :canonical: simplemseed.fdsnsourceid.bandCodeForRate

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.bandCodeForRate

.. py:function:: bandCodeInfo(bandCode: str)
   :canonical: simplemseed.fdsnsourceid.bandCodeInfo

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.bandCodeInfo

.. py:data:: bandcodes_file
   :canonical: simplemseed.fdsnsourceid.bandcodes_file
   :value: None

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.bandcodes_file

.. py:function:: do_parseargs()
   :canonical: simplemseed.fdsnsourceid.do_parseargs

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.do_parseargs

.. py:function:: loadBandCodes()
   :canonical: simplemseed.fdsnsourceid.loadBandCodes

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.loadBandCodes

.. py:function:: loadSourceCodes()
   :canonical: simplemseed.fdsnsourceid.loadSourceCodes

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.loadSourceCodes

.. py:function:: main()
   :canonical: simplemseed.fdsnsourceid.main

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.main

.. py:function:: sourceCodeDescribe(sourceCode: str) -> str
   :canonical: simplemseed.fdsnsourceid.sourceCodeDescribe

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.sourceCodeDescribe

.. py:function:: sourceCodeInfo(sourceCode: str)
   :canonical: simplemseed.fdsnsourceid.sourceCodeInfo

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.sourceCodeInfo

.. py:data:: sourcecodes_file
   :canonical: simplemseed.fdsnsourceid.sourcecodes_file
   :value: None

   .. autodoc2-docstring:: simplemseed.fdsnsourceid.sourcecodes_file
