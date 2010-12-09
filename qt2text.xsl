<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" />
  
  <xsl:template match="/">
      <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="author">
    <xsl:text>&#9;--</xsl:text>
    <xsl:apply-templates />
  </xsl:template>

  <xsl:template match="source">
    <xsl:text>&#9;--</xsl:text>
    <xsl:apply-templates />
  </xsl:template>

  <!-- Text highlighting -->

  <xsl:template match="em">
    <xsl:text> *</xsl:text>
    <xsl:apply-templates />
    <xsl:text>* </xsl:text>
  </xsl:template>
  
  <xsl:template match="cite | foreign">
    <xsl:text> _</xsl:text>
    <xsl:apply-templates />
    <xsl:text>_ </xsl:text>
  </xsl:template>

  <xsl:template match="pre | code">
    <xsl:text> </xsl:text>
    <xsl:apply-templates />
    <xsl:text> </xsl:text>
  </xsl:template>


</xsl:stylesheet>
